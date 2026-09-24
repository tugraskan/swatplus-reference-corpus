/**
 * Pure JSON types, argv builders, and grouping logic for the `swatref` CLI.
 *
 * No `vscode` import here: this module is unit-tested without a VS Code host
 * (see src/test/swatref.test.ts) and holds no process or UI concerns.
 */

export interface SourceProfile {
	name: string;
	repository: string;
	ref: string;
	commit: string;
	label: string;
	checkout: string;
	fetched: boolean;
	docs_default: boolean;
	schema_default: boolean;
}

export interface RemoteRef {
	ref: string;
	commit: string;
	release?: boolean;
}

export interface RemoteRefs {
	tags: RemoteRef[];
	branches: RemoteRef[];
}

export interface AddResult {
	profile: string;
	created: boolean;
	moved: boolean;
	commit: string;
	current_commit: string;
	ref: string;
	repository: string;
	checkout: string;
}

function isRecord(value: unknown): value is Record<string, unknown> {
	return typeof value === 'object' && value !== null;
}

export function isSourceProfile(value: unknown): value is SourceProfile {
	if (!isRecord(value)) {
		return false;
	}
	return (
		typeof value.name === 'string' &&
		typeof value.repository === 'string' &&
		typeof value.ref === 'string' &&
		typeof value.commit === 'string' &&
		typeof value.label === 'string' &&
		typeof value.checkout === 'string' &&
		typeof value.fetched === 'boolean' &&
		typeof value.docs_default === 'boolean' &&
		typeof value.schema_default === 'boolean'
	);
}

export function isSourceProfileList(value: unknown): value is SourceProfile[] {
	return Array.isArray(value) && value.every(isSourceProfile);
}

function isRemoteRef(value: unknown, requireRelease: boolean): value is RemoteRef {
	if (!isRecord(value)) {
		return false;
	}
	if (typeof value.ref !== 'string' || typeof value.commit !== 'string') {
		return false;
	}
	return !requireRelease || typeof value.release === 'boolean';
}

export function isRemoteRefs(value: unknown): value is RemoteRefs {
	if (!isRecord(value)) {
		return false;
	}
	return (
		Array.isArray(value.tags) &&
		value.tags.every(t => isRemoteRef(t, true)) &&
		Array.isArray(value.branches) &&
		value.branches.every(b => isRemoteRef(b, false))
	);
}

export function isAddResult(value: unknown): value is AddResult {
	if (!isRecord(value)) {
		return false;
	}
	return (
		typeof value.profile === 'string' &&
		typeof value.created === 'boolean' &&
		typeof value.moved === 'boolean' &&
		typeof value.commit === 'string' &&
		typeof value.current_commit === 'string' &&
		typeof value.ref === 'string' &&
		typeof value.repository === 'string' &&
		typeof value.checkout === 'string'
	);
}

export const RELEASE_TAG_RE = /^v?\d+(\.\d+)+$/;
const RELEASE_TAG_CAPTURE_RE = /^v?(\d+(?:\.\d+)+)$/;

export function isReleaseTag(ref: string): boolean {
	return RELEASE_TAG_RE.test(ref);
}

/**
 * The version schema build would derive on its own (mirrors
 * source/config.py's with_schema_source): the release tag without a
 * leading "v", or undefined when `ref` is not a release tag at all.
 */
export function releaseVersionFromRef(ref: string): string | undefined {
	return RELEASE_TAG_CAPTURE_RE.exec(ref)?.[1];
}

export interface GroupedRefs {
	releases: RemoteRef[];
	otherTags: RemoteRef[];
	branches: RemoteRef[];
}

export function groupRemoteRefs(refs: RemoteRefs): GroupedRefs {
	return {
		releases: refs.tags.filter(t => t.release === true),
		otherTags: refs.tags.filter(t => t.release !== true),
		branches: refs.branches,
	};
}

export function pullRequestRef(prNumber: string): string {
	return `refs/pull/${prNumber}/head`;
}

export function pythonModuleArgs(args: string[]): string[] {
	return ['-m', 'swatplus_reference.cli', ...args];
}

export function sourceListArgs(): string[] {
	return ['source', 'list'];
}

export function sourceRefsArgs(): string[] {
	return ['source', 'refs'];
}

export function sourceAddArgs(ref: string, name?: string): string[] {
	return name ? ['source', 'add', ref, '--name', name] : ['source', 'add', ref];
}

export function sourceFetchArgs(profile: string): string[] {
	return ['source', 'fetch', profile];
}

export function schemaBuildArgs(profile: string, version?: string): string[] {
	return version
		? ['schema', 'build', '--source', profile, '--version', version]
		: ['schema', 'build', '--source', profile];
}

export function docsSnapshotArgs(profile: string): string[] {
	return ['docs', 'rich-parse', '--snapshot', '--source', profile];
}

export interface CompareOptions {
	buildSources: boolean;
	buildPreview: boolean;
}

export function compareArgs(base: string, candidate: string, options: CompareOptions): string[] {
	const args = ['compare', '--fetch', '--base', base, '--candidate', candidate];
	if (!options.buildSources) {
		args.push('--skip-source-build');
	}
	if (!options.buildPreview) {
		args.push('--skip-preview');
	}
	return args;
}

export function schemaOutputPath(version: string): string {
	return `schema_artifacts/releases/swatplus-${version}.json`;
}

export function snapshotsDirPath(): string {
	return 'snapshots/rich';
}

export function comparisonSummaryPath(base: string, candidate: string): string {
	return `reports/comparisons/${base}_vs_${candidate}/summary.md`;
}

export function shortCommit(commit: string): string {
	return commit.slice(0, 12);
}

/** The last non-empty line of stderr, for a one-line error notification. */
export function lastNonEmptyLine(text: string): string | undefined {
	const lines = text.split('\n').map(l => l.trim()).filter(l => l.length > 0);
	return lines.length > 0 ? lines[lines.length - 1] : undefined;
}
