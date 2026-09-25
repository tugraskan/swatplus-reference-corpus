/** Registers swatplusCorpus.* commands: the three flows, plus fetch/refresh/showOutput. */

import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { checkPrerequisites, loadSourceList, reportFailure, runSwatref } from './runner';
import { SourceItem, SourcesTreeProvider } from './sourcesTree';
import {
	AddResult,
	CompareOptions,
	RemoteRefs,
	SourceProfile,
	comparisonSummaryPath,
	compareArgs,
	compareOutcome,
	docsSnapshotArgs,
	groupRemoteRefs,
	isAddResult,
	isRemoteRefs,
	pullRequestRef,
	releaseVersionFromRef,
	pythonModuleArgs,
	schemaBuildArgs,
	schemaOutputPath,
	shortCommit,
	snapshotsDirPath,
	sourceAddArgs,
	sourceFetchArgs,
	sourceRefsArgs,
} from './swatref';

interface Ctx {
	pythonExecutable: string;
	corpusRoot: string;
	outputChannel: vscode.OutputChannel;
}

export function registerCommands(
	context: vscode.ExtensionContext,
	tree: SourcesTreeProvider,
	outputChannel: vscode.OutputChannel,
	getCorpusRoot: () => string | undefined
): void {
	const resolveCtx = async (): Promise<Ctx | undefined> => {
		const corpusRoot = getCorpusRoot();
		if (!corpusRoot) {
			void vscode.window.showInformationMessage(
				'Open a workspace folder containing swatref.toml to use SWAT+ Corpus commands.'
			);
			return undefined;
		}
		const pythonPathSetting = vscode.workspace.getConfiguration('swatplusCorpus').get<string>('pythonPath');
		const status = checkPrerequisites(pythonPathSetting || undefined);
		if (!status.ready || !status.pythonExecutable) {
			const choice = await vscode.window.showErrorMessage(status.message, 'Copy install command');
			if (choice === 'Copy install command') {
				await vscode.env.clipboard.writeText('pip install -e .');
			}
			return undefined;
		}
		return { pythonExecutable: status.pythonExecutable, corpusRoot, outputChannel };
	};

	context.subscriptions.push(
		vscode.commands.registerCommand('swatplusCorpus.addVersion', async () => {
			const ctx = await resolveCtx();
			if (ctx) {
				await addVersion(ctx, tree);
			}
		}),
		vscode.commands.registerCommand('swatplusCorpus.build', async (item?: SourceItem) => {
			const ctx = await resolveCtx();
			if (ctx) {
				await build(ctx, tree, item?.profile.name);
			}
		}),
		vscode.commands.registerCommand('swatplusCorpus.compare', async (item?: SourceItem) => {
			const ctx = await resolveCtx();
			if (ctx) {
				await compare(ctx, tree, item?.profile.name);
			}
		}),
		vscode.commands.registerCommand('swatplusCorpus.fetch', async (item?: SourceItem) => {
			const ctx = await resolveCtx();
			if (!ctx) {
				return;
			}
			const name = item?.profile.name ?? (await pickProfile(ctx, 'Pick a profile to fetch'))?.name;
			if (name) {
				await fetchProfile(ctx, tree, name);
			}
		}),
		vscode.commands.registerCommand('swatplusCorpus.refresh', () => tree.refresh()),
		vscode.commands.registerCommand('swatplusCorpus.showOutput', () => outputChannel.show(true))
	);
}

function toQuickPickItem(p: SourceProfile): vscode.QuickPickItem & { profile: SourceProfile } {
	return {
		label: p.name,
		description: `${p.ref} · ${shortCommit(p.commit)}`,
		detail: p.label,
		profile: p,
	};
}

async function pickProfileFrom(list: SourceProfile[], placeHolder: string): Promise<SourceProfile | undefined> {
	const picked = await vscode.window.showQuickPick(list.map(toQuickPickItem), { placeHolder });
	return picked?.profile;
}

async function pickProfile(ctx: Ctx, placeHolder: string): Promise<SourceProfile | undefined> {
	const list = await loadSourceList(ctx.pythonExecutable, ctx.corpusRoot, ctx.outputChannel);
	if (!list) {
		return undefined;
	}
	return pickProfileFrom(list, placeHolder);
}

type RefPickItem = vscode.QuickPickItem & { ref?: string; action?: 'pr' | 'other' };

async function pickRef(ctx: Ctx): Promise<string | undefined> {
	const result = await vscode.window.withProgress(
		{ location: vscode.ProgressLocation.Notification, title: 'Loading SWAT+ tags and branches…' },
		() => runSwatref(ctx.pythonExecutable, pythonModuleArgs(sourceRefsArgs()), ctx.corpusRoot, ctx.outputChannel)
	);
	if (result.status !== 0) {
		await reportFailure(ctx.outputChannel, result, 'swatref source refs');
		return undefined;
	}
	let refs: RemoteRefs;
	try {
		const data: unknown = JSON.parse(result.stdout);
		if (!isRemoteRefs(data)) {
			void vscode.window.showErrorMessage('Unexpected response from `swatref source refs`.');
			return undefined;
		}
		refs = data;
	} catch {
		void vscode.window.showErrorMessage('Could not parse `swatref source refs` output.');
		return undefined;
	}

	const grouped = groupRemoteRefs(refs);
	const items: RefPickItem[] = [];
	const addGroup = (label: string, entries: { ref: string; commit: string }[]) => {
		if (entries.length === 0) {
			return;
		}
		items.push({ label, kind: vscode.QuickPickItemKind.Separator });
		items.push(...entries.map(e => ({ label: e.ref, description: shortCommit(e.commit), ref: e.ref })));
	};
	addGroup('Releases', grouped.releases);
	addGroup('Other tags', grouped.otherTags);
	addGroup('Branches', grouped.branches);
	items.push({ label: '', kind: vscode.QuickPickItemKind.Separator });
	items.push({ label: 'Pull request number…', action: 'pr' });
	items.push({ label: 'Other ref or commit…', action: 'other' });

	const picked = await vscode.window.showQuickPick(items, {
		placeHolder: 'Pick a SWAT+ release, tag, branch, or pull request',
	});
	if (!picked) {
		return undefined;
	}
	if (picked.action === 'pr') {
		const prNumber = await vscode.window.showInputBox({
			prompt: 'Pull request number',
			validateInput: v => (/^\d+$/.test(v) ? undefined : 'Digits only'),
		});
		return prNumber ? pullRequestRef(prNumber) : undefined;
	}
	if (picked.action === 'other') {
		return vscode.window.showInputBox({ prompt: 'Branch, tag, or commit' });
	}
	return picked.ref;
}

async function addVersion(ctx: Ctx, tree: SourcesTreeProvider): Promise<void> {
	const ref = await pickRef(ctx);
	if (!ref) {
		return;
	}

	const result = await vscode.window.withProgress(
		{ location: vscode.ProgressLocation.Notification, title: `Adding ${ref}…` },
		() => runSwatref(ctx.pythonExecutable, pythonModuleArgs(sourceAddArgs(ref)), ctx.corpusRoot, ctx.outputChannel)
	);
	if (result.status !== 0) {
		await reportFailure(ctx.outputChannel, result, 'swatref source add');
		return;
	}

	let added: AddResult;
	try {
		const data: unknown = JSON.parse(result.stdout);
		if (!isAddResult(data)) {
			void vscode.window.showErrorMessage('Unexpected response from `swatref source add`.');
			return;
		}
		added = data;
	} catch {
		void vscode.window.showErrorMessage('Could not parse `swatref source add` output.');
		return;
	}

	tree.refresh();

	if (added.created) {
		const choice = await vscode.window.showInformationMessage(
			`Added \`${added.profile}\` locked at \`${shortCommit(added.commit)}\`.`,
			'Build…'
		);
		if (choice === 'Build…') {
			await build(ctx, tree, added.profile);
		}
	} else if (added.moved) {
		await vscode.window.showWarningMessage(
			`\`${added.profile}\` is locked at \`${shortCommit(added.commit)}\`; ` +
				`\`${added.ref}\` is now at \`${shortCommit(added.current_commit)}\`.`
		);
	} else {
		await vscode.window.showInformationMessage(`\`${added.profile}\` is already configured.`);
	}
}

type BuildStep = 'schema' | 'docs';

async function build(ctx: Ctx, tree: SourcesTreeProvider, presetProfileName?: string): Promise<void> {
	let profile: SourceProfile | undefined;
	if (presetProfileName) {
		const list = await loadSourceList(ctx.pythonExecutable, ctx.corpusRoot, ctx.outputChannel);
		profile = list?.find(p => p.name === presetProfileName);
	} else {
		profile = await pickProfile(ctx, 'Pick a profile to build');
	}
	if (!profile) {
		return;
	}

	const stepItems: (vscode.QuickPickItem & { step: BuildStep })[] = [
		{ label: 'Input schema', picked: true, step: 'schema' },
		{ label: 'Docs snapshot', picked: true, step: 'docs' },
	];
	const chosen = await vscode.window.showQuickPick(stepItems, {
		canPickMany: true,
		placeHolder: `Build ${profile.name}`,
	});
	if (!chosen || chosen.length === 0) {
		return;
	}
	const steps = new Set(chosen.map(c => c.step));

	// `versionArg` is passed as --version only when the CLI can't derive it
	// itself; `resolvedVersion` is what the build will actually be named,
	// known either way, and used below to reveal the right schema file.
	let versionArg: string | undefined;
	let resolvedVersion: string | undefined;
	if (steps.has('schema')) {
		resolvedVersion = releaseVersionFromRef(profile.ref);
		if (!resolvedVersion) {
			const typed = await vscode.window.showInputBox({
				prompt: `Schema version for ${profile.name} (its ref "${profile.ref}" is not a release tag)`,
				value: profile.name,
			});
			if (!typed) {
				// Cancelling the version box cancels the whole build.
				return;
			}
			versionArg = typed;
			resolvedVersion = typed;
		}
	}

	const plan: { label: string; argv: string[] }[] = [];
	if (!profile.fetched) {
		plan.push({ label: `Fetching ${profile.name}…`, argv: sourceFetchArgs(profile.name) });
	}
	if (steps.has('schema')) {
		plan.push({ label: 'Building input schema…', argv: schemaBuildArgs(profile.name, versionArg) });
	}
	if (steps.has('docs')) {
		plan.push({ label: 'Building docs snapshot…', argv: docsSnapshotArgs(profile.name) });
	}

	type Outcome = { kind: 'ok' } | { kind: 'cancelled' } | { kind: 'failed'; label: string; result: Awaited<ReturnType<typeof runSwatref>> };
	const outcome = await vscode.window.withProgress<Outcome>(
		{ location: vscode.ProgressLocation.Notification, title: `Building ${profile.name}`, cancellable: true },
		async (progress, token) => {
			for (const step of plan) {
				progress.report({ message: step.label });
				const result = await runSwatref(
					ctx.pythonExecutable,
					pythonModuleArgs(step.argv),
					ctx.corpusRoot,
					ctx.outputChannel,
					token
				);
				if (result.cancelled) {
					return { kind: 'cancelled' };
				}
				if (result.status !== 0) {
					return { kind: 'failed', label: step.label, result };
				}
			}
			return { kind: 'ok' };
		}
	);

	if (outcome.kind === 'cancelled') {
		return;
	}
	if (outcome.kind === 'failed') {
		await reportFailure(ctx.outputChannel, outcome.result, outcome.label.replace(/…$/, ''));
		return;
	}

	tree.refresh();
	const buttons: string[] = [];
	if (steps.has('schema')) {
		buttons.push('Reveal schema');
	}
	if (steps.has('docs')) {
		buttons.push('Reveal snapshots');
	}
	const choice = await vscode.window.showInformationMessage(`Built ${profile.name}.`, ...buttons);
	if (choice === 'Reveal schema' && resolvedVersion) {
		await revealPath(ctx.corpusRoot, schemaOutputPath(resolvedVersion));
	} else if (choice === 'Reveal snapshots') {
		await revealPath(ctx.corpusRoot, snapshotsDirPath());
	}
}

async function fetchProfile(ctx: Ctx, tree: SourcesTreeProvider, profileName: string): Promise<void> {
	const result = await vscode.window.withProgress(
		{ location: vscode.ProgressLocation.Notification, title: `Fetching ${profileName}…`, cancellable: true },
		(progress, token) =>
			runSwatref(ctx.pythonExecutable, pythonModuleArgs(sourceFetchArgs(profileName)), ctx.corpusRoot, ctx.outputChannel, token)
	);
	if (result.cancelled) {
		return;
	}
	if (result.status !== 0) {
		await reportFailure(ctx.outputChannel, result, `swatref source fetch ${profileName}`);
		return;
	}
	tree.refresh();
}

async function compare(ctx: Ctx, tree: SourcesTreeProvider, presetCandidateName?: string): Promise<void> {
	const list = await loadSourceList(ctx.pythonExecutable, ctx.corpusRoot, ctx.outputChannel);
	if (!list) {
		return;
	}

	let base: SourceProfile | undefined;
	let candidate: SourceProfile | undefined;
	if (presetCandidateName) {
		candidate = list.find(p => p.name === presetCandidateName);
		if (!candidate) {
			return;
		}
		base = await pickProfileFrom(
			list.filter(p => p.name !== candidate!.name),
			`Pick a base to compare against ${candidate.name}`
		);
	} else {
		base = await pickProfileFrom(list, 'Pick a base version');
		if (!base) {
			return;
		}
		candidate = await pickProfileFrom(
			list.filter(p => p.name !== base!.name),
			'Pick a candidate version'
		);
	}
	if (!base || !candidate) {
		return;
	}

	const optionItems: (vscode.QuickPickItem & { key: keyof CompareOptions })[] = [
		{ label: 'Compile both sources (needs CMake + gfortran)', picked: false, key: 'buildSources' },
		{ label: 'Build strict docs preview (MkDocs)', picked: false, key: 'buildPreview' },
	];
	const chosen = await vscode.window.showQuickPick(optionItems, {
		canPickMany: true,
		placeHolder: 'Comparison options (default: fast path)',
	});
	if (!chosen) {
		return;
	}
	const options: CompareOptions = {
		buildSources: chosen.some(c => c.key === 'buildSources'),
		buildPreview: chosen.some(c => c.key === 'buildPreview'),
	};

	const startedAt = Date.now();
	const result = await vscode.window.withProgress(
		{ location: vscode.ProgressLocation.Notification, title: `Comparing ${base.name} → ${candidate.name}`, cancellable: true },
		(progress, token) =>
			runSwatref(
				ctx.pythonExecutable,
				pythonModuleArgs(compareArgs(base!.name, candidate!.name, options)),
				ctx.corpusRoot,
				ctx.outputChannel,
				token
			)
	);
	if (result.cancelled) {
		return;
	}

	tree.refresh();
	const summaryPath = comparisonSummaryPath(base.name, candidate.name);
	const outcome = compareOutcome(result.status, fileMtimeMs(ctx.corpusRoot, summaryPath), startedAt);
	if (outcome === 'complete') {
		await openMarkdownPreview(ctx.corpusRoot, summaryPath);
	} else if (outcome === 'incomplete') {
		await openMarkdownPreview(ctx.corpusRoot, summaryPath);
		await vscode.window.showWarningMessage('Comparison incomplete: see summary.');
	} else {
		await reportFailure(ctx.outputChannel, result, 'swatref compare');
	}
}

function fileMtimeMs(corpusRoot: string, relativePath: string): number | undefined {
	try {
		return fs.statSync(path.join(corpusRoot, relativePath)).mtimeMs;
	} catch {
		return undefined;
	}
}

async function revealPath(corpusRoot: string, relativePath: string): Promise<void> {
	const uri = vscode.Uri.file(path.join(corpusRoot, relativePath));
	await vscode.commands.executeCommand('revealFileInOS', uri);
}

async function openMarkdownPreview(corpusRoot: string, relativePath: string): Promise<void> {
	const uri = vscode.Uri.file(path.join(corpusRoot, relativePath));
	await vscode.commands.executeCommand('markdown.showPreview', uri);
}
