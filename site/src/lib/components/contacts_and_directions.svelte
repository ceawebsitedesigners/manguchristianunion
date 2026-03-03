<section id="contact-section">

    <!-- Contact info -->
    <div class="contact-block">
        <h1>Contact Us Today</h1>

        <div class="contact-items">
            <div class="contact-item">
                <span class="contact-icon">📞</span>
                <div class="contact-details">
                    <span class="contact-label">Patron</span>
                    <a href="tel:0123456789" class="contact-value">0123 456 789</a>
                </div>
            </div>

            <div class="contact-item">
                <span class="contact-icon">📞</span>
                <div class="contact-details">
                    <span class="contact-label">Matron</span>
                    <a href="tel:9876543210" class="contact-value">9876 543 210</a>
                </div>
            </div>

            <div class="contact-item">
                <span class="contact-icon">✉️</span>
                <div class="contact-details">
                    <span class="contact-label">Email</span>
                    <a href="mailto:example@email.com" class="contact-value">example@email.com</a>
                </div>
            </div>
        </div>
    </div>

    <!-- Directions -->
    <div class="directions-block">
        <h1>Visit Us</h1>
        <p>
            We are located at Mang'u High School, off Thika Road.
            Come find us and join our family.
        </p>
        <a href="https://www.google.com/maps/place/Mangu+High+School/@-1.0740984,37.0440477,17z/data=!3m1!4b1!4m6!3m5!1s0x182f4fe077a6466b:0x849bc00dffb03c40!8m2!3d-1.0740984!4d37.0466226!16s%2Fm%2F02rdl_l?entry=ttu&g_ep=EgoyMDI2MDEyOC4wIKXMDSoASAFQAw%3D%3D" target="_blank" rel="noopener noreferrer" class="directions-btn">
            📍 Get Directions
        </a>
    </div>

</section>

<style>
    /* ── Section wrapper ── */
    #contact-section {
        display: flex;
        flex-direction: row;
        width: 100%;
        min-height: 320px;
    }

    /* ── Left: Contact block ── */
    .contact-block {
        flex: 1;
        background-color: #faf6ee;
        padding: 5vh 5vw;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    /* ── Right: Directions block ── */
    .directions-block {
        flex: 1;
        background-color: #1a1a1a;
        padding: 5vh 5vw;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    /* ── Shared heading ── */
    h1 {
        color: #d4a017;
        font-size: clamp(1.6rem, 3vw, 2.4rem);
        font-weight: 700;
        margin-bottom: 1.6rem;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    /* ── Contact item row ── */
    .contact-items {
        display: flex;
        flex-direction: column;
        gap: 1.2rem;
    }

    .contact-item {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .contact-icon {
        font-size: 1.5rem;
        flex-shrink: 0;
    }

    .contact-details {
        display: flex;
        flex-direction: column;
        gap: 0.1rem;
    }

    .contact-label {
        font-size: clamp(0.72rem, 1.1vw, 0.8rem);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #888;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    .contact-value {
        font-size: clamp(0.95rem, 1.6vw, 1.05rem);
        color: #3a3838;
        text-decoration: none;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        transition: color 0.2s ease;
    }

    .contact-value:hover {
        color: #d4a017;
    }

    /* ── Directions text ── */
    .directions-block p {
        font-size: clamp(0.95rem, 1.7vw, 1.05rem);
        line-height: 1.7;
        color: rgba(255, 255, 255, 0.75);
        margin-bottom: 1.8rem;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }

    /* ── Get Directions button ── */
    .directions-btn {
        display: inline-block;
        width: fit-content;
        background-color: #d4a017;
        color: #1a1a1a;
        font-weight: 700;
        font-size: clamp(0.88rem, 1.3vw, 0.97rem);
        padding: 0.75rem 1.6rem;
        border-radius: 8px;
        text-decoration: none;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                     'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        transition: background-color 0.2s ease, transform 0.2s ease;
    }

    .directions-btn:hover {
        background-color: #b8890f;
        transform: translateY(-2px);
    }

    /* ── Responsive ── */
    @media (max-width: 680px) {
        #contact-section {
            flex-direction: column;
        }

        .contact-block,
        .directions-block {
            padding: 5vh 7vw;
        }
    }
</style>
