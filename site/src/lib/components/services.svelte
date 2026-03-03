<section id="services-section">

    <div id="heading">
        <h1>Our Services & Events</h1>
        <p>
            Join us as we worship together, grow in faith, and build
            community. Everyone is welcome to be part of our church family.
        </p>
    </div>

    <div id="services">
        <div class="card">
            <div class="card-icon">☀️</div>
            <h2>Sunday Service</h2>
            <p class="time">8:00 AM – 10:00 AM</p>
            <p class="desc">
                Join us for inspiring worship, powerful preaching,
                and meaningful fellowship with our church family.
            </p>
            <ul>
                <li>Contemporary Worship</li>
                <li>Biblical Teaching</li>
                <li>Prayer &amp; Fellowship</li>
            </ul>
        </div>

        <div class="card">
            <div class="card-icon">🙏</div>
            <h2>Midweek Prayer</h2>
            <p class="time">1:00 PM – 2:00 PM</p>
            <p class="desc">
                Come together for corporate prayer, spiritual growth,
                and community fellowship.
            </p>
            <ul>
                <li>Community Prayer</li>
                <li>Spiritual Meditation</li>
                <li>Fellowship</li>
            </ul>
        </div>

        <div class="card">
            <div class="card-icon">📖</div>
            <h2>Sunday School</h2>
            <p class="time">8:00 AM – 10:00 AM</p>
            <p class="desc">
                Educational programs for all children to learn and
                grow in faith together.
            </p>
            <ul>
                <li>Age-Appropriate Learning</li>
                <li>Interactive Teaching</li>
                <li>Character Building</li>
            </ul>
        </div>
    </div>
</section>

<style>
    /* ── Section wrapper ── */
    #services-section {
        width: 100%;
        padding: 7vh 5vw;
        background-color: #faf8f4;
    }

    /* ── Heading block ── */
    #heading {
        text-align: center;
        max-width: 580px;
        margin: 0 auto 5vh;
    }

    #heading h1 {
        color: #d4a017;
        font-size: clamp(2rem, 4.5vw, 3.2rem);
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 1rem;
    }

    #heading p {
        font-size: clamp(0.95rem, 1.8vw, 1.1rem);
        line-height: 1.7;
        color: #3a3838;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    /* ── Cards row ── */
    #services {
        display: flex;
        flex-direction: row;
        gap: 1.6rem;
        max-width: 1100px;
        margin: 0 auto;
    }

    /* ── Individual card ── */
    .card {
        flex: 1;
        min-width: 0;
        background-color: #ffffff;
        border: 1px solid #000000;
        border-radius: 14px;
        padding: 2rem 1.6rem 1.8rem;
        display: flex;
        flex-direction: column;
        transition: box-shadow 0.25s ease, transform 0.25s ease;
    }

    .card:hover {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.09);
        transform: translateY(-4px);
        border: 3px solid #000000;
    }

    /* ── Card icon ── */
    .card-icon {
        font-size: 1.8rem;
        margin-bottom: 0.8rem;
    }

    /* ── Card title ── */
    .card h2 {
        font-size: clamp(1.1rem, 1.8vw, 1.35rem);
        color: #d4a017;
        font-weight: 600;
        margin-bottom: 0.3rem;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    /* ── Time label ── */
    .time {
        font-size: clamp(0.8rem, 1.2vw, 0.9rem);
        color: #888;
        font-weight: 500;
        margin-bottom: 0.9rem;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    /* ── Description ── */
    .desc {
        font-size: clamp(0.88rem, 1.4vw, 0.98rem);
        line-height: 1.6;
        color: #4a4848;
        margin-bottom: 1.1rem;
        flex-grow: 1;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    /* ── Feature list ── */
    ul {
        list-style: none;
        padding: 0;
        margin: 0;
        border-top: 1px solid #ede8dc;
        padding-top: 1rem;
    }

    ul li {
        position: relative;
        padding-left: 1.2rem;
        font-size: clamp(0.82rem, 1.2vw, 0.92rem);
        color: #5a5656;
        line-height: 1.8;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    ul li::before {
        content: '✓';
        position: absolute;
        left: 0;
        color: #d4a017;
        font-weight: 700;
    }

    /* ── Responsive ── */
    @media (max-width: 768px) {
        #services {
            flex-direction: column;
            gap: 1.2rem;
        }

        #services-section {
            padding: 6vh 6vw;
        }
    }
</style>
