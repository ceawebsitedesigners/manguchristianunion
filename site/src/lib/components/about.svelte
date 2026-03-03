<script>
    import About_Image from '../assets/about-image.jpg';
</script>

<section id="about">
    <div id="text">
        <h1 id="main_title">About Our Church</h1>

        <p class="description">
            Mang'u Christian Union has been a beacon of hope and faith in our community
            for years. We are more than just a church – we are a family united
            by our love for Christ and our commitment to serving others. Our mission is
            to create a welcoming environment where people from all walks of life can experience God's
            transforming love, grow in their faith, and discover their purpose in God's kingdom.
        </p>

        <section id="cards">
            <div class="card-row">
                <div class="card" id="love">
                    <h2>Love & Compassion</h2>
                    <p>We believe in showing Christ's love
                       through our actions and care for one
                       another.
                    </p>
                </div>
                <div class="card" id="community">
                    <h2>Community</h2>
                    <p>
                        Building strong relationships and supporting
                        each other in our spiritual journey.
                    </p>
                </div>
            </div>
            <div class="card-row">
                <div class="card" id="biblical_truth">
                    <h2>Biblical Truth</h2>
                    <p>Grounded in Scripture and committed to
                        teaching God's Word with clarity and
                        passion.
                    </p>
                </div>
                <div class="card" id="faith">
                    <h2>Faith</h2>
                    <p>
                        Deepening our relationship with Jesus
                        Christ and living out our faith daily.
                    </p>
                </div>
            </div>
        </section>
    </div>

    <div id="image">
        <img src={About_Image} alt="About our church" />
    </div>
</section>

<style>
    /* ── Layout ── */
    #about {
        display: flex;
        flex-direction: row;
        min-height: 100vh;
        width: 100%;
    }

    #text {
        flex: 1;
        padding: 6vh 4vw;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    /* ── Title ── */
    #main_title {
        color: #d4a017;
        margin-bottom: 3vh;
        font-size: clamp(2.5rem, 5vw, 4rem);
        font-weight: 700;
        line-height: 1.2;
    }

    /* ── Description ── */
    .description {
        font-size: clamp(0.95rem, 1.8vw, 1.1rem);
        line-height: 1.7;
        color: #3a3838;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        max-width: 540px;
    }

    /* ── Cards Grid ── */
    #cards {
        display: flex;
        flex-direction: column;
        gap: 1.2rem;
        margin-top: 4vh;
    }

    .card-row {
        display: flex;
        flex-direction: row;
        gap: 1.2rem;
    }

    /* ── Individual Cards ── */
    .card {
        background-color: #faf6ee;
        border: 1px solid #ede8dc;
        border-radius: 12px;
        padding: 1.6rem 1.4rem;
        flex: 1;
        min-width: 0;
        transition: box-shadow 0.25s ease, transform 0.25s ease;
    }

    .card:hover {
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        transform: translateY(-3px);
    }

    .card h2 {
        font-size: clamp(1rem, 1.6vw, 1.2rem);
        color: #d4a017;
        margin-bottom: 0.6rem;
        font-weight: 600;
    }

    .card p {
        font-size: clamp(0.85rem, 1.3vw, 0.95rem);
        line-height: 1.6;
        color: #4a4848;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    /* ── Image Panel ── */
    #image {
        width: 42%;
        min-height: 100vh;
        overflow: hidden;
    }

    #image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
    }

    /* ── Responsive ── */
    @media (max-width: 768px) {
        #about {
            flex-direction: column;
        }

        #image {
            width: 100%;
            height: 40vh;
            min-height: unset;
        }

        #text {
            padding: 5vh 6vw;
        }

        .card-row {
            flex-direction: column;
        }
    }
</style>
