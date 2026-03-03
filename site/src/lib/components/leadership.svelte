<script lang="ts">
    // ── Types ──────────────────────────────────────
    interface Leader {
        chairman: string;
        deputyChairman: string;
        treasurer: string;
        secretary: string;
        churchManager: string;
        praiseAndWorship: string[];
        choirMaster: string;
        discipleship: string[]; // [senior, junior]
        bibleStudy: string[];   // [senior, junior]
        churchengineer: String[]; //[senior , junior]
    }

    interface YearData {
        theme: string;
        leaders: Leader;
    }

    // ── Mock Data ──────────────────────────────────
    const leadershipData: Record<string, YearData> = {
        '2026': {
            theme: 'Walking in Faith',
            leaders: {
                chairman: 'Oliver Mwangi',
                deputyChairman: 'Grace Njeri',
                treasurer: 'David Kamau',
                secretary: 'Faith Akinyi',
                churchManager: 'Peter Otieno',
                praiseAndWorship: ['Sarah Wanjiku', 'John Kimani', 'Mary Achieng'],
                choirMaster: 'James Odhiambo',
                discipleship: ['Senior: Mark Karanja', 'Junior: Anne Muthoni'],
                bibleStudy: ['Senior: Paul Njoroge', 'Junior: Ruth Wambui'],
                churchengineer: ['Senior: Mark']

            }
        },
        '2025': {
            theme: 'God of Miracles',
            leaders: {
                chairman: 'Samuel Omondi',
                deputyChairman: 'Esther Wangari',
                treasurer: 'Joseph Kiprop',
                secretary: 'Lucy Chebet',
                churchManager: 'Daniel Mutua',
                praiseAndWorship: ['Agnes Nekesa', 'Timothy Kibet'],
                choirMaster: 'Michael Rotich',
                discipleship: ['Senior: Isaac Korir', 'Junior: Rebecca Nyambura'],
                bibleStudy: ['Senior: Stephen Juma', 'Junior: Hannah Wairimu'],
                churchengineer: ['Senior: Mark']

            }
        }
    };

    // ── State ──────────────────────────────────────
    let selectedYear = '2026';
    let showMore = false;

    // ── Computed values ────────────────────────────
    $: currentData = leadershipData[selectedYear];
    $: availableYears = Object.keys(leadershipData).sort().reverse();
</script>

<!-- ────────────────────────────────────────────── -->
<section id="leadership-section">

    <div id="heading">
        <h1>Church Leadership</h1>
        <p>
            To ensure the church runs smoothly, a team of God-fearing leaders
            are chosen to serve the Lord and His people.
        </p>
    </div>

    <!-- Year selector -->
    <div id="year-selector">
        <label for="year-select">Select Year:</label>
        <select id="year-select" bind:value={selectedYear}>
            {#each availableYears as year}
                <option value={year}>{year}</option>
            {/each}
        </select>
    </div>

    <!-- Theme -->
    <div id="theme">
        <h2>{currentData.theme}</h2>
    </div>

    <!-- Main 4 leaders -->
    <div id="leaders-grid">
        <div class="card">
            <h3>Chairman</h3>
            <p class="leader-name">👤 {currentData.leaders.chairman}</p>
        </div>

        <div class="card">
            <h3>Deputy Chairman</h3>
            <p class="leader-name">👤 {currentData.leaders.deputyChairman}</p>
        </div>

        <div class="card">
            <h3>Treasurer</h3>
            <p class="leader-name">👤 {currentData.leaders.treasurer}</p>
        </div>

        <div class="card">
            <h3>Secretary</h3>
            <p class="leader-name">👤 {currentData.leaders.secretary}</p>
        </div>
    </div>

    <!-- View More toggle -->
    <div id="view-more-toggle">
        <button on:click={() => showMore = !showMore}>
            {showMore ? '▲ Show Less' : '▼ View More Leaders'}
        </button>
    </div>

    <!-- Collapsible extra leaders -->
    {#if showMore}
        <div id="extra-leaders" class="fade-in">
            <div class="card">
                <h3>Church Manager</h3>
                <p class="leader-name">👤 {currentData.leaders.churchManager}</p>
            </div>

            <div class="card">
                <h3>Choir Master</h3>
                <p class="leader-name">👤 {currentData.leaders.choirMaster}</p>
            </div>

            <div class="card">
                <h3>Praise &amp; Worship Team</h3>
                {#each currentData.leaders.praiseAndWorship as member}
                    <p class="team-member">👤 {member}</p>
                {/each}
            </div>

            <div class="card">
                <h3>Discipleship</h3>
                {#each currentData.leaders.discipleship as leader}
                    <p class="team-member">👤 {leader}</p>
                {/each}
            </div>

            <div class="card">
                <h3>Bible Study</h3>
                {#each currentData.leaders.bibleStudy as leader}
                    <p class="team-member">👤 {leader}</p>
                {/each}
            </div>
            <div class="card">
                <h3>Church Engineer</h3>
                {#each currentData.leaders.churchengineer as leader}
                    <p class="team-member">👤 {leader}</p>
                {/each}
            </div>
        </div>
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
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    #heading p {
        font-size: clamp(0.95rem, 1.7vw, 1.05rem);
        color: #3a3838;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
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
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    #year-selector select {
        font-size: clamp(0.9rem, 1.4vw, 1rem);
        padding: 0.5rem 1rem;
        border: 1px solid #ede8dc;
        border-radius: 8px;
        background-color: #ffffff;
        color: #3a3838;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
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
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
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
        transition: box-shadow 0.25s ease, transform 0.25s ease;
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
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    .leader-name {
        font-size: clamp(0.9rem, 1.4vw, 1rem);
        color: #3a3838;
        margin: 0;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    .team-member {
        font-size: clamp(0.85rem, 1.3vw, 0.95rem);
        color: #4a4848;
        margin: 0.3rem 0;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
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
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        transition: background-color 0.2s ease, transform 0.2s ease;
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
        margin: 0 auto;
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
</style>
