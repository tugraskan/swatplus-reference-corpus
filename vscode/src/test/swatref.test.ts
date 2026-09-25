import * as assert from 'assert';
import {
	compareOutcome,
	RELEASE_TAG_RE,
	compareArgs,
	docsSnapshotArgs,
	groupRemoteRefs,
	isAddResult,
	isReleaseTag,
	isRemoteRefs,
	isSourceProfile,
	isSourceProfileList,
	pullRequestRef,
	pythonModuleArgs,
	releaseVersionFromRef,
	schemaBuildArgs,
	schemaOutputPath,
	shortCommit,
	sourceAddArgs,
	sourceFetchArgs,
	sourceListArgs,
	sourceRefsArgs,
	comparisonSummaryPath,
	lastNonEmptyLine,
} from '../swatref';

const SOURCE_LIST_FIXTURE = [
	{
		name: 'release_62_0_0',
		repository: 'https://github.com/swat-model/swatplus',
		ref: '62.0.0',
		commit: 'de210d64db4f1d75e110bd6af33ea9c333d27b8a',
		label: 'SWAT+ 62.0.0',
		checkout: 'external/swatplus-62.0.0',
		fetched: true,
		docs_default: false,
		schema_default: true,
	},
];

const REFS_FIXTURE = {
	tags: [
		{ ref: '63.0.0', commit: 'aaaa', release: true },
		{ ref: '62.0.0', commit: 'bbbb', release: true },
		{ ref: 'nightly-2026-01-01', commit: 'cccc', release: false },
	],
	branches: [{ ref: 'main', commit: 'dddd' }, { ref: 'dev', commit: 'eeee' }],
};

const ADD_RESULT_FIXTURE = {
	profile: 'release_63_0_0',
	created: true,
	moved: false,
	commit: 'ffff000011112222333344445555666677778888',
	current_commit: 'ffff000011112222333344445555666677778888',
	ref: '63.0.0',
	repository: 'https://github.com/swat-model/swatplus',
	checkout: 'external/swatplus-release_63_0_0',
};

suite('swatref argv builders', () => {
	test('module-form prefix wraps flow args with -m swatplus_reference.cli', () => {
		assert.deepStrictEqual(pythonModuleArgs(sourceListArgs()), ['-m', 'swatplus_reference.cli', 'source', 'list']);
	});

	test('source list / refs', () => {
		assert.deepStrictEqual(sourceListArgs(), ['source', 'list']);
		assert.deepStrictEqual(sourceRefsArgs(), ['source', 'refs']);
	});

	test('source add without and with an explicit name', () => {
		assert.deepStrictEqual(sourceAddArgs('63.0.0'), ['source', 'add', '63.0.0']);
		assert.deepStrictEqual(sourceAddArgs('refs/pull/252/head', 'pr_252'), [
			'source',
			'add',
			'refs/pull/252/head',
			'--name',
			'pr_252',
		]);
	});

	test('source fetch', () => {
		assert.deepStrictEqual(sourceFetchArgs('release_62_0_0'), ['source', 'fetch', 'release_62_0_0']);
	});

	test('schema build omits --version for a release-tag profile', () => {
		assert.deepStrictEqual(schemaBuildArgs('release_62_0_0'), ['schema', 'build', '--source', 'release_62_0_0']);
	});

	test('schema build passes --version when given', () => {
		assert.deepStrictEqual(schemaBuildArgs('dev_pr252_base', '63.0.0'), [
			'schema',
			'build',
			'--source',
			'dev_pr252_base',
			'--version',
			'63.0.0',
		]);
	});

	test('docs snapshot', () => {
		assert.deepStrictEqual(docsSnapshotArgs('main'), ['docs', 'rich-parse', '--snapshot', '--source', 'main']);
	});

	test('compare defaults to both --skip-* flags (the fast path)', () => {
		assert.deepStrictEqual(compareArgs('dev_pr252_base', 'pr_252', { buildSources: false, buildPreview: false }), [
			'compare',
			'--fetch',
			'--base',
			'dev_pr252_base',
			'--candidate',
			'pr_252',
			'--skip-source-build',
			'--skip-preview',
		]);
	});

	test('compare drops a --skip-* flag once its option is selected', () => {
		assert.deepStrictEqual(compareArgs('a', 'b', { buildSources: true, buildPreview: false }), [
			'compare',
			'--fetch',
			'--base',
			'a',
			'--candidate',
			'b',
			'--skip-preview',
		]);
		assert.deepStrictEqual(compareArgs('a', 'b', { buildSources: false, buildPreview: true }), [
			'compare',
			'--fetch',
			'--base',
			'a',
			'--candidate',
			'b',
			'--skip-source-build',
		]);
		assert.deepStrictEqual(compareArgs('a', 'b', { buildSources: true, buildPreview: true }), [
			'compare',
			'--fetch',
			'--base',
			'a',
			'--candidate',
			'b',
		]);
	});
});

suite('release-tag regex', () => {
	test('accepts release tags with and without a leading v', () => {
		assert.ok(isReleaseTag('62.0.0'));
		assert.ok(isReleaseTag('v62.0.0'));
		assert.ok(isReleaseTag('61.0.2.61'));
		assert.ok(RELEASE_TAG_RE.test('1.0'));
	});

	test('rejects branches, PR refs, and commits', () => {
		assert.ok(!isReleaseTag('main'));
		assert.ok(!isReleaseTag('dev'));
		assert.ok(!isReleaseTag('refs/pull/252/head'));
		assert.ok(!isReleaseTag('cb442f7c05fc3bfc34349c446010f452d2737ca0'));
	});
});

suite('releaseVersionFromRef (what `schema build` derives without --version)', () => {
	test('strips a leading v and passes a bare tag through', () => {
		assert.strictEqual(releaseVersionFromRef('v62.0.0'), '62.0.0');
		assert.strictEqual(releaseVersionFromRef('62.0.0'), '62.0.0');
		assert.strictEqual(releaseVersionFromRef('61.0.2.61'), '61.0.2.61');
	});

	test('is undefined for anything that is not a release tag', () => {
		assert.strictEqual(releaseVersionFromRef('main'), undefined);
		assert.strictEqual(releaseVersionFromRef('refs/pull/252/head'), undefined);
	});
});

suite('QuickPick grouping of a `source refs` payload', () => {
	test('splits tags into releases and other tags, keeps branches separate', () => {
		const grouped = groupRemoteRefs(REFS_FIXTURE);
		assert.deepStrictEqual(
			grouped.releases.map(r => r.ref),
			['63.0.0', '62.0.0']
		);
		assert.deepStrictEqual(
			grouped.otherTags.map(r => r.ref),
			['nightly-2026-01-01']
		);
		assert.deepStrictEqual(
			grouped.branches.map(r => r.ref),
			['main', 'dev']
		);
	});

	test('pullRequestRef builds refs/pull/<n>/head', () => {
		assert.strictEqual(pullRequestRef('252'), 'refs/pull/252/head');
	});
});

suite('JSON type guards reject malformed payloads', () => {
	test('isSourceProfileList accepts the documented shape', () => {
		assert.ok(isSourceProfileList(SOURCE_LIST_FIXTURE));
		assert.ok(isSourceProfile(SOURCE_LIST_FIXTURE[0]));
	});

	test('isSourceProfileList rejects a missing field, wrong type, or non-array', () => {
		const { fetched, ...missingFetched } = SOURCE_LIST_FIXTURE[0];
		void fetched;
		assert.ok(!isSourceProfileList([missingFetched]));
		assert.ok(!isSourceProfileList([{ ...SOURCE_LIST_FIXTURE[0], fetched: 'yes' }]));
		assert.ok(!isSourceProfileList({ not: 'an array' }));
		assert.ok(!isSourceProfileList(null));
	});

	test('isRemoteRefs accepts the documented shape and rejects a tag missing `release`', () => {
		assert.ok(isRemoteRefs(REFS_FIXTURE));
		assert.ok(!isRemoteRefs({ tags: [{ ref: '1.0.0', commit: 'aaaa' }], branches: [] }));
		assert.ok(!isRemoteRefs({ tags: [] }));
	});

	test('isAddResult accepts the documented shape and rejects a malformed payload', () => {
		assert.ok(isAddResult(ADD_RESULT_FIXTURE));
		const { moved, ...missingMoved } = ADD_RESULT_FIXTURE;
		void moved;
		assert.ok(!isAddResult(missingMoved));
		assert.ok(!isAddResult('not an object'));
		assert.ok(!isAddResult(undefined));
	});
});

suite('output locations and small formatters', () => {
	test('schemaOutputPath', () => {
		assert.strictEqual(schemaOutputPath('62.0.0'), 'schema_artifacts/releases/swatplus-62.0.0.json');
	});

	test('comparisonSummaryPath', () => {
		assert.strictEqual(comparisonSummaryPath('dev_pr252_base', 'pr_252'), 'reports/comparisons/dev_pr252_base_vs_pr_252/summary.md');
	});

	test('shortCommit truncates to 12 characters', () => {
		assert.strictEqual(shortCommit('de210d64db4f1d75e110bd6af33ea9c333d27b8a'), 'de210d64db4f');
	});

	test('lastNonEmptyLine returns the final non-blank stderr line', () => {
		assert.strictEqual(lastNonEmptyLine('a\nb\n\n'), 'b');
		assert.strictEqual(lastNonEmptyLine('   \n'), undefined);
	});
});

suite('compareOutcome', () => {
	const started = 1_000_000;

	test('a summary this run wrote follows the exit code', () => {
		assert.strictEqual(compareOutcome(0, started + 5_000, started), 'complete');
		assert.strictEqual(compareOutcome(1, started + 5_000, started), 'incomplete');
		assert.strictEqual(compareOutcome(2, started + 5_000, started), 'failed');
	});

	test('a crash (exit 1) never shows an older run\'s summary', () => {
		assert.strictEqual(compareOutcome(1, started - 60_000, started), 'failed');
		assert.strictEqual(compareOutcome(0, started - 60_000, started), 'failed');
	});

	test('no summary at all is a failure', () => {
		assert.strictEqual(compareOutcome(1, undefined, started), 'failed');
		assert.strictEqual(compareOutcome(null, undefined, started), 'failed');
	});
});
