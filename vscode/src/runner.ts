/**
 * Find Python, check prerequisites, and run `swatref` with live output and a
 * working Cancel button. Adapted from swatplus-dataselector's src/indexer.ts
 * (getPythonCandidates, getIndexingPrerequisiteStatus, runPythonIndexer).
 */

import * as vscode from 'vscode';
import { spawn, spawnSync } from 'child_process';
import {
	isSourceProfileList,
	lastNonEmptyLine,
	pythonModuleArgs,
	sourceListArgs,
	SourceProfile,
} from './swatref';

export interface PrerequisiteStatus {
	ready: boolean;
	message: string;
	missingModules: string[];
	pythonExecutable?: string;
}

export interface RunResult {
	status: number | null;
	stdout: string;
	stderr: string;
	startError?: Error;
	cancelled: boolean;
}

const PREREQUISITE_CACHE_TTL_MS = 10_000;
let prerequisiteCache: { checkedAt: number; status: PrerequisiteStatus } | undefined;

/** swatplusCorpus.pythonPath setting, then SWATPLUS_PYTHON, then the platform default. */
export function getPythonCandidates(pythonPathSetting?: string): string[] {
	const candidates: string[] = [];
	if (pythonPathSetting) {
		candidates.push(pythonPathSetting);
	}
	if (process.env.SWATPLUS_PYTHON) {
		candidates.push(process.env.SWATPLUS_PYTHON);
	}
	if (process.platform === 'win32') {
		candidates.push('py', 'python', 'python3');
	} else {
		candidates.push('python3', 'python');
	}
	return Array.from(new Set(candidates));
}

function extractMissingModules(text: string): string[] {
	const modules = new Set<string>();
	for (const match of text.matchAll(/No module named ['"]([^'"]+)['"]/g)) {
		if (match[1]) {
			modules.add(match[1]);
		}
	}
	return Array.from(modules);
}

/** Checks `import swatplus_reference` against each Python candidate, cached for 10s. */
export function checkPrerequisites(pythonPathSetting?: string, forceRefresh = false): PrerequisiteStatus {
	const now = Date.now();
	if (!forceRefresh && prerequisiteCache && now - prerequisiteCache.checkedAt < PREREQUISITE_CACHE_TTL_MS) {
		return prerequisiteCache.status;
	}

	const candidates = getPythonCandidates(pythonPathSetting);
	const missingModules = new Set<string>();
	let pythonFound = false;
	let lastError = '';

	for (const pythonExecutable of candidates) {
		let result;
		try {
			result = spawnSync(pythonExecutable, ['-c', 'import swatplus_reference'], {
				encoding: 'utf-8',
				timeout: 4000,
			});
		} catch (error) {
			lastError = error instanceof Error ? error.message : String(error);
			continue;
		}

		if (result.error) {
			if ((result.error as NodeJS.ErrnoException).code !== 'ENOENT') {
				lastError = result.error.message;
			}
			continue;
		}

		pythonFound = true;
		if (result.status === 0) {
			const status: PrerequisiteStatus = {
				ready: true,
				message: 'Python and swatplus_reference are available.',
				missingModules: [],
				pythonExecutable,
			};
			prerequisiteCache = { checkedAt: now, status };
			return status;
		}

		const output = `${result.stderr || ''}\n${result.stdout || ''}`.trim();
		extractMissingModules(output).forEach(m => missingModules.add(m));
		lastError = output || `${pythonExecutable} exited with code ${result.status}`;
	}

	const missingModuleList = Array.from(missingModules);
	let message: string;
	if (!pythonFound) {
		message = 'Python was not found. Install Python 3.10+ to use the SWAT+ Corpus extension.';
	} else if (missingModuleList.length > 0) {
		message = `Python is available but swatplus_reference is missing. Install with: pip install -e .`;
	} else {
		message = `swatplus_reference prerequisite check failed${lastError ? `: ${lastError}` : '.'}`;
	}

	const status: PrerequisiteStatus = { ready: false, message, missingModules: missingModuleList };
	prerequisiteCache = { checkedAt: now, status };
	return status;
}

/**
 * Run `python <argv>` in `cwd`, streaming stdout/stderr to `outputChannel` as
 * it arrives and killing the child if `token` is cancelled.
 */
export function runSwatref(
	pythonExecutable: string,
	argv: string[],
	cwd: string,
	outputChannel: vscode.OutputChannel,
	token?: vscode.CancellationToken
): Promise<RunResult> {
	return new Promise(resolve => {
		let stdout = '';
		let stderr = '';
		let cancelled = false;
		let settled = false;

		outputChannel.appendLine(`$ ${pythonExecutable} ${argv.join(' ')}`);

		let child: import('child_process').ChildProcessWithoutNullStreams;
		try {
			child = spawn(pythonExecutable, argv, { cwd, windowsHide: true });
		} catch (err) {
			resolve({
				status: null,
				stdout: '',
				stderr: '',
				startError: err instanceof Error ? err : new Error(String(err)),
				cancelled: false,
			});
			return;
		}

		const cancelSubscription = token?.onCancellationRequested(() => {
			cancelled = true;
			// SIGTERM lets Python unwind; the process is killed outright if it ignores it.
			// Not `child.killed`: that turns true once SIGTERM is *sent*, so it
			// would never let the SIGKILL through.
			child.kill('SIGTERM');
			setTimeout(() => {
				if (!settled && child.exitCode === null && child.signalCode === null) {
					child.kill('SIGKILL');
				}
			}, 2000).unref?.();
		});

		const settle = (result: { status: number | null; stdout: string; stderr: string; startError?: Error }) => {
			if (settled) {
				return;
			}
			settled = true;
			cancelSubscription?.dispose();
			resolve({ ...result, cancelled });
		};

		child.stdout.setEncoding('utf-8');
		child.stderr.setEncoding('utf-8');
		child.stdout.on('data', (chunk: string) => {
			stdout += chunk;
			outputChannel.append(chunk);
		});
		child.stderr.on('data', (chunk: string) => {
			stderr += chunk;
			outputChannel.append(chunk);
		});
		child.on('error', err => settle({ status: null, stdout, stderr, startError: err }));
		child.on('close', code => settle({ status: code, stdout, stderr }));
	});
}

/** Exit codes: 0 success; 1 comparison incomplete; 2 bad args/failed step. Shows the last stderr line. */
export async function reportFailure(
	outputChannel: vscode.OutputChannel,
	result: RunResult,
	contextLabel: string
): Promise<void> {
	if (result.cancelled) {
		return;
	}
	const message = result.startError
		? `${contextLabel}: ${result.startError.message}`
		: `${contextLabel} failed: ${lastNonEmptyLine(result.stderr) ?? `exit code ${result.status}`}`;
	const choice = await vscode.window.showErrorMessage(message, 'Show output');
	if (choice === 'Show output') {
		outputChannel.show(true);
	}
}

/** Runs `source list` and parses its JSON, reporting any failure. */
export async function loadSourceList(
	pythonExecutable: string,
	corpusRoot: string,
	outputChannel: vscode.OutputChannel
): Promise<SourceProfile[] | undefined> {
	const result = await runSwatref(pythonExecutable, pythonModuleArgs(sourceListArgs()), corpusRoot, outputChannel);
	if (result.status !== 0) {
		await reportFailure(outputChannel, result, 'swatref source list');
		return undefined;
	}
	try {
		const data = JSON.parse(result.stdout);
		if (!isSourceProfileList(data)) {
			void vscode.window.showErrorMessage('Unexpected response from `swatref source list`.');
			return undefined;
		}
		return data;
	} catch {
		void vscode.window.showErrorMessage('Could not parse `swatref source list` output.');
		return undefined;
	}
}
