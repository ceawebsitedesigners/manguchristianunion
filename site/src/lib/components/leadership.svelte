<script lang="ts">
	
	import { browser } from '$app/environment';
	import { URLS } from '$lib/urls';
	import {
		leadershipStore,
		getLeadershipFromLocal,
		saveLeadershipToLocal,
		type YearData
	} from '$lib/stores';

	function formatLabel(key: string) {
		const result = key.replace(/([A-Z])/g, ' $1');
		return result.charAt(0).toUpperCase() + result.slice(1);
	}

	// ── State ──────────────────────────────────────
	let selectedYear = new Date().getFullYear().toString();
	let showMore = false;
	let currentData: YearData | null = null;
	let isLoading = true;
	let error: string | null = null;
	let cache: Record<string, YearData> = {};

	// Subscribe to store
	leadershipStore.subscribe((value) => {
		cache = value;
		if (selectedYear && cache[selectedYear]) {
			currentData = cache[selectedYear];
			isLoading = false;
		}
	});

	if (browser) {
		const localCache = getLeadershipFromLocal();
		if (localCache) {
			for (const [year, data] of Object.entries(localCache)) {
				leadershipStore.addYear(year, data);
			}
		}
	}

	// Default to last 5 years for the dropdown
	let availableYears = Array.from({ length: 5 }, (_, i) =>
		(new Date().getFullYear() - i).toString()
	);

	// ── API Call ───────────────────────────────────
	async function fetchLeadershipData(year: string) {
		// Always clear error and reset state before any early returns
		error = null;
		currentData = null;

		// 1. Check in-memory cache first
		if (cache[year]) {
			currentData = cache[year];
			isLoading = false;
			return;
		}

		isLoading = true;
		try {
			const res = await fetch(`${URLS.leadership}?year=${year}`);
			if (!res.ok) {
				throw new Error(`Failed to fetch data: ${res.statusText}`);
			}
			const data = await res.json();

			if (!data || Object.keys(data).length === 0) {
				currentData = null;
			} else {
				currentData = data;
				// 2. Save to store and local storage
				leadershipStore.addYear(year, data);
				saveLeadershipToLocal({ ...cache, [year]: data });
			}
		} catch (err: unknown) {
			const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
			console.error(err);
			error = errorMessage;
			currentData = null;
		} finally {
			isLoading = false;
		}
	}

	$: if (selectedYear) {
		fetchLeadershipData(selectedYear);
	}

	const extraRolesOrder = [
		'prayerCoordinator',
		'assistantPrayerCoordinators',
		'choirMaster',
		'assistantChoirMaster',
		'praiseAndWorshipCoordinators',
		'talentsCoordinator',
		'assistantTalentsCoordinator',
		'bibleStudyCoordinators',
		'believersCoordinators',
		'assistantBelieversCoordinators',
		'childrensMinistry',
		'churchCoordinators',
		'followUpCoordinators',
		'royalPriesthood',
		'engineers'
	];

	$: extraLeaders = currentData
		? (() => {
				const leadersObj = currentData.leaders || {};
				const mainRoles = ['chairman', 'deputyChairman', 'treasurer', 'secretary'];
				const result = [];

				// 1. Add known roles in order
				for (const role of extraRolesOrder) {
					if (leadersObj[role] !== undefined) {
						result.push({ key: role, value: leadersObj[role] });
					}
				}

				// 2. Add any remaining dynamically fetched roles not mapped
				for (const [k, v] of Object.entries(leadersObj)) {
					if (!mainRoles.includes(k) && !extraRolesOrder.includes(k)) {
						result.push({ key: k, value: v });
					}
				}

				return result;
			})()
		: [];
</script>

<!-- ────────────────────────────────────────────── -->
<section id="leadership-section">
	<div id="heading">
		<h1>Church Leadership</h1>
		<p>
			To ensure the church runs smoothly, a team of God-fearing leaders are chosen to serve the Lord
			and His people.
		</p>
	</div>

	<!-- Year selector -->
	<div id="year-selector">
		<label for="year-select">Select Year:</label>
		<select id="year-select" bind:value={selectedYear}>
			{#each availableYears as year (year)}
				<option value={year}>{year}</option>
			{/each}
		</select>
	</div>

	<!-- Theme -->
	{#if isLoading}
		<div class="status-message">Loading leadership info...</div>
	{:else if error}
		<div class="status-message error">Error: {error}</div>
	{:else if currentData}
		<div id="theme">
			<h2>{currentData.theme}</h2>
		</div>

		<!-- Main 4 leaders -->
		<div id="leaders-grid">
			<div class="card">
				<h3>Chairman</h3>
				<p class="leader-name">👤 {currentData.leaders?.chairman || 'TBD'}</p>
			</div>

			<div class="card">
				<h3>Deputy Chairman</h3>
				<p class="leader-name">👤 {currentData.leaders?.deputyChairman || 'TBD'}</p>
			</div>

			<div class="card">
				<h3>Treasurer</h3>
				<p class="leader-name">👤 {currentData.leaders?.treasurer || 'TBD'}</p>
			</div>

			<div class="card">
				<h3>Secretary</h3>
				<p class="leader-name">👤 {currentData.leaders?.secretary || 'TBD'}</p>
			</div>
		</div>

		<!-- Collapsible extra leaders -->
		{#if showMore}
			<div id="extra-leaders" class="fade-in">
				{#each extraLeaders as { key, value } (key)}
					<div class="card">
						<h3>{formatLabel(key)}</h3>
						{#if typeof value === 'string'}
							<p class="leader-name">👤 {value || 'TBD'}</p>
						{:else if Array.isArray(value) && value.length > 0}
							{#each value as member (member)}
								<p class="team-member">👤 {member}</p>
							{/each}
						{:else}
							<p class="leader-name">TBD</p>
						{/if}
					</div>
				{/each}
			</div>
		{/if}

		<!-- View More toggle -->
		<div id="view-more-toggle">
			<button on:click={() => (showMore = !showMore)}>
				{showMore ? '▲ Show Less' : '▼ View More Leaders'}
			</button>
		</div>
	{:else}
		<div class="status-message">No leadership information available for {selectedYear}.</div>
	{/if}
</section>

<style>
	/* ── Section wrapper ── */
	#leadership-section {
		width: 100%;
		padding: 7vh 5vw;
		background-color: #faf8f4;
	}

	/* ── Heading ── */
	#heading {
		text-align: center;
		max-width: 580px;
		margin: 0 auto 3vh;
	}

	#heading h1 {
		color: #d4a017;
		font-size: clamp(2rem, 4.5vw, 3.2rem);
		font-weight: 700;
		line-height: 1.2;
		margin-bottom: 0.7rem;
		font-family:
			'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana,
			sans-serif;
	}

	#heading p {
		font-size: clamp(0.95rem, 1.7vw, 1.05rem);
		color: #3a3838;
		font-family:
			'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana,
			sans-serif;
	}

	/* ── Year selector ── */
	#year-selector {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.8rem;
		margin-bottom: 2vh;
	}

	#year-selector label {
		font-size: clamp(0.9rem, 1.4vw, 1rem);
		font-weight: 600;
		color: #3a3838;
		font-family:
			'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana,
			sans-serif;
	}

	#year-selector select {
		font-size: clamp(0.9rem, 1.4vw, 1rem);
		padding: 0.5rem 1rem;
		border: 1px solid #ede8dc;
		border-radius: 8px;
		background-color: #ffffff;
		color: #3a3838;
		font-family:
			'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana,
			sans-serif;
		cursor: pointer;
		transition: border-color 0.2s ease;
	}

	#year-selector select:hover {
		border-color: #d4a017;
	}

	/* ── Theme ── */
	#theme {
		text-align: center;
		margin-bottom: 4vh;
	}

	#theme h2 {
		font-size: clamp(1.3rem, 2.5vw, 1.8rem);
		color: #d4a017;
		font-weight: 600;
		font-style: italic;
		font-family:
			'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana,
			sans-serif;
	}

	/* ── Leaders grid ── */
	#leaders-grid {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 1.4rem;
		max-width: 1100px;
		margin: 0 auto 3vh;
	}

	/* ── Card ── */
	.card {
		background-color: #ffffff;
		border: 1px solid #ede8dc;
		border-radius: 14px;
		padding: 1.8rem 1.4rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		text-align: center;
		transition:
			box-shadow 0.25s ease,
			transform 0.25s ease;
	}

	.card:hover {
		box-shadow: 0 8px 24px rgba(0, 0, 0, 0.09);
		transform: translateY(-4px);
	}

	.card h3 {
		font-size: clamp(1rem, 1.5vw, 1.2rem);
		color: #d4a017;
		font-weight: 600;
		margin-bottom: 0.8rem;
		font-family:
			'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana,
			sans-serif;
	}

	.leader-name {
		font-size: clamp(0.9rem, 1.4vw, 1rem);
		color: #3a3838;
		margin: 0;
		font-family:
			'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana,
			sans-serif;
	}

	.team-member {
		font-size: clamp(0.85rem, 1.3vw, 0.95rem);
		color: #4a4848;
		margin: 0.3rem 0;
		font-family:
			'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana,
			sans-serif;
	}

	/* ── View More toggle ── */
	#view-more-toggle {
		display: flex;
		justify-content: center;
		margin-bottom: 3vh;
	}

	#view-more-toggle button {
		background-color: #d4a017;
		color: #1a1a1a;
		border: none;
		font-weight: 700;
		font-size: clamp(0.88rem, 1.3vw, 0.97rem);
		padding: 0.75rem 1.6rem;
		border-radius: 8px;
		cursor: pointer;
		font-family:
			'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana,
			sans-serif;
		transition:
			background-color 0.2s ease,
			transform 0.2s ease;
	}

	#view-more-toggle button:hover {
		background-color: #b8890f;
		transform: translateY(-2px);
	}

	/* ── Extra leaders grid ── */
	#extra-leaders {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 1.4rem;
		max-width: 1100px;
		margin: 0 auto 3vh;
	}

	/* ── Fade-in animation ── */
	.fade-in {
		animation: fadeIn 0.4s ease;
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(-10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	/* ── Responsive ── */
	@media (max-width: 900px) {
		#leaders-grid {
			grid-template-columns: repeat(2, 1fr);
		}

		#extra-leaders {
			grid-template-columns: repeat(2, 1fr);
		}
	}

	@media (max-width: 520px) {
		#leaders-grid,
		#extra-leaders {
			grid-template-columns: 1fr;
		}

		#leadership-section {
			padding: 6vh 6vw;
		}
	}

	/* ── Status Messages ── */
	.status-message {
		text-align: center;
		padding: 40px;
		font-size: 1.1rem;
		color: #4a4848;
		font-family:
			'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana,
			sans-serif;
	}

	.status-message.error {
		color: #d32f2f;
	}
</style>