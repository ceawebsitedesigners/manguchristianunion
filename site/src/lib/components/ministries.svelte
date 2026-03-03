<section id="ministries-section">

    <div id="description">
        <h1>Our Ministries</h1>
        <p>
            Discover your place in our church family. Whether you're
            looking to grow spiritually, serve others, or
            connect with fellow believers, we have a ministry
            for you.
        </p>
    </div>

    <div id="ministries">

        <div class="card">
            <div class="card-icon">🎵</div>
            <h2>Praise &amp; Worship Team</h2>
            <span class="badge">25+ Members</span>
            <p>
                Leading our congregation in heartfelt worship
                through music, helping create an atmosphere
                where God is glorified.
            </p>
        </div>

        <div class="card">
            <div class="card-icon">👧</div>
            <h2>Children's Ministry</h2>
            <p>
                Nurturing children in their faith journey through
                age-appropriate lessons, activities, and care in
                a safe environment.
            </p>
        </div>

        <div class="card">
            <div class="card-icon">🎨</div>
            <h2>Talents Ministry</h2>
            <span class="badge">40+ Members</span>
            <p>
                Discovering and developing God-given talents and
                gifts within our congregation for ministry and
                service to the church.
            </p>
        </div>

        <div class="card">
            <div class="card-icon">🤝</div>
            <h2>Discipleship Ministry</h2>
            <p>
                Supporting new believers and members through
                discipleship, mentoring, and spiritual growth
                programs.
            </p>
        </div>

    </div>
</section>

<style>
    /* ── Section wrapper ── */
    #ministries-section {
        width: 100%;
        padding: 7vh 5vw;
        background-color: #ffffff;
    }

    /* ── Heading block ── */
    #description {
        text-align: center;
        max-width: 580px;
        margin: 0 auto 5vh;
    }

    #description h1 {
        color: #d4a017;
        font-size: clamp(2rem, 4.5vw, 3.2rem);
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 1rem;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    #description p {
        font-size: clamp(0.95rem, 1.8vw, 1.1rem);
        line-height: 1.7;
        color: #3a3838;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    /* ── Cards grid ── */
    #ministries {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.4rem;
        max-width: 1100px;
        margin: 0 auto;
    }

    /* ── Individual card ── */
    .card {
        background-color: #faf6ee;
        border: 1px solid #ede8dc;
        border-radius: 14px;
        padding: 1.8rem 1.4rem;
        display: flex;
        flex-direction: column;
        transition: box-shadow 0.25s ease, transform 0.25s ease;
    }

    .card:hover {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.09);
        transform: translateY(-4px);
    }

    /* ── Card icon ── */
    .card-icon {
        font-size: 1.8rem;
        margin-bottom: 0.7rem;
    }

    /* ── Card title ── */
    .card h2 {
        font-size: clamp(1rem, 1.5vw, 1.2rem);
        color: #d4a017;
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    /* ── Member badge ── */
    .badge {
        display: inline-block;
        width: fit-content;
        background-color: #d4a01715;
        color: #b08510;
        font-size: clamp(0.75rem, 1.1vw, 0.82rem);
        font-weight: 600;
        padding: 0.25rem 0.7rem;
        border-radius: 20px;
        margin-bottom: 0.8rem;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    /* ── Description ── */
    .card p {
        font-size: clamp(0.85rem, 1.3vw, 0.95rem);
        line-height: 1.65;
        color: #4a4848;
        flex-grow: 1;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    /* ── Responsive ── */
    @media (max-width: 900px) {
        #ministries {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    @media (max-width: 520px) {
        #ministries {
            grid-template-columns: 1fr;
        }

        #ministries-section {
            padding: 6vh 6vw;
        }
    }
</style>
