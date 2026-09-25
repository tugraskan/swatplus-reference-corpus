/** activate(): register the Sources tree and the swatplusCorpus.* commands. */

import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { registerCommands } from './commands';
import { SourcesTreeProvider } from './sourcesTree';

/** The first workspace folder that contains swatref.toml, or undefined. */
function findCorpusRoot(): string | undefined {
	const folders = vscode.workspace.workspaceFolders;
	if (!folders) {
		return undefined;
	}
	for (const folder of folders) {
		if (fs.existsSync(path.join(folder.uri.fsPath, 'swatref.toml'))) {
			return folder.uri.fsPath;
		}
	}
	return undefined;
}

export function activate(context: vscode.ExtensionContext): void {
	const outputChannel = vscode.window.createOutputChannel('SWAT+ Corpus');
	context.subscriptions.push(outputChannel);

	const treeProvider = new SourcesTreeProvider(findCorpusRoot, outputChannel);
	const treeView = vscode.window.createTreeView('swatplusCorpusSources', {
		treeDataProvider: treeProvider,
	});
	treeProvider.attachView(treeView);
	context.subscriptions.push(treeView);

	context.subscriptions.push(
		vscode.workspace.onDidChangeWorkspaceFolders(() => treeProvider.refresh())
	);

	registerCommands(context, treeProvider, outputChannel, findCorpusRoot);
}

export function deactivate(): void {}
