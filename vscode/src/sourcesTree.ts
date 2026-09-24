/** TreeDataProvider over `swatref source list`. */

import * as vscode from 'vscode';
import { checkPrerequisites, loadSourceList } from './runner';
import { shortCommit, SourceProfile } from './swatref';

export class SourceItem extends vscode.TreeItem {
	constructor(public readonly profile: SourceProfile) {
		super(profile.name, vscode.TreeItemCollapsibleState.None);
		let description = `${profile.ref} · ${shortCommit(profile.commit)}`;
		if (profile.docs_default) {
			description += ' (docs)';
		}
		if (profile.schema_default) {
			description += ' (schema)';
		}
		this.description = description;
		this.tooltip = profile.label;
		this.iconPath = new vscode.ThemeIcon(profile.fetched ? 'check' : 'cloud-download');
		this.contextValue = 'swatplusCorpusSource';
	}
}

export class SourcesTreeProvider implements vscode.TreeDataProvider<SourceItem> {
	private readonly changeEmitter = new vscode.EventEmitter<void>();
	readonly onDidChangeTreeData = this.changeEmitter.event;
	private view?: vscode.TreeView<SourceItem>;

	constructor(
		private readonly getCorpusRoot: () => string | undefined,
		private readonly outputChannel: vscode.OutputChannel
	) {}

	attachView(view: vscode.TreeView<SourceItem>): void {
		this.view = view;
	}

	refresh(): void {
		this.changeEmitter.fire();
	}

	getTreeItem(element: SourceItem): vscode.TreeItem {
		return element;
	}

	async getChildren(): Promise<SourceItem[]> {
		const corpusRoot = this.getCorpusRoot();
		if (!corpusRoot) {
			this.setMessage('Open a workspace folder containing swatref.toml.');
			return [];
		}

		const pythonPathSetting = vscode.workspace.getConfiguration('swatplusCorpus').get<string>('pythonPath');
		const status = checkPrerequisites(pythonPathSetting || undefined);
		if (!status.ready || !status.pythonExecutable) {
			this.setMessage(status.message);
			return [];
		}

		const profiles = await loadSourceList(status.pythonExecutable, corpusRoot, this.outputChannel);
		if (!profiles) {
			this.setMessage('Could not load source profiles. See the SWAT+ Corpus output for details.');
			return [];
		}

		this.setMessage(undefined);
		return profiles.map(p => new SourceItem(p));
	}

	private setMessage(message: string | undefined): void {
		if (this.view) {
			this.view.message = message;
		}
	}
}
