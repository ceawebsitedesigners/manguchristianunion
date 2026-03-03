<section id="hero">
  <div id="hero-inner">
    <div class="title-block">
      <h1 class="title-main">MANG'U</h1>
      <h1 class="title-sub">CHRISTIAN UNION</h1>
    </div>

    <p>
      Join our vibrant community of faith where every heart finds hope,
      every soul discovers purpose, and every life is transformed by God's
      amazing grace.
    </p>
  </div>
</section>

<style>
  /* ── Hero wrapper ── */
  #hero {
    position: relative;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
  }

  /* ── Background image layer ── */
  #hero-inner {
    position: relative;
    width: 100%;
    height: 100%;

    background-image: url("../assets/hero-church.jpg");
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 1;
  }

  /* ── Dark overlay (pseudo-element) ── */
  #hero-inner::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(
      to bottom, 
      rgb(255, 230, 0) 0%,
      rgba(250, 226, 16, 0.7) 50%,
      rgba(255, 237, 36, 0.3) 100%
      );
    /* background: linear-gradient(
      to bottom,
      rgba(0, 0, 0, 0.45) 0%,
      rgba(0, 0, 0, 0.6) 50%,
      rgba(0, 0, 0, 0.7) 100%
    ); */
    z-index: 0;
  }

  /* ── Content sits above the overlay ── */
  .title-block,
  p {
    position: relative;
    z-index: 1;
   
  }

  /* ── Title group ── */
  .title-block {
    text-align: center;
    animation: fadeSlideDown 1s ease forwards;
  }

  .title-main {
    overflow: hidden;
    font-size: clamp(3.5rem, 10vw, 8rem);
    font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    font-weight: 700;
    color: #0a0a0a;
    line-height: 1;
    letter-spacing: 0.08em;
    text-shadow: 0 2px 16px rgba(0, 0, 0, 0.4);
    margin-bottom: 0.15em;
  }

  .title-sub {
    font-size: clamp(1.4rem, 4vw, 2.8rem);
    font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    font-weight: 400;
    color: #ffffff;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
  }

  /* ── Tagline paragraph ── */
  p {
    margin-top: 3.5vh;
    max-width: 560px;
    text-align: center;
    font-size: clamp(0.95rem, 1.8vw, 1.15rem);
    line-height: 1.75;
    color: rgba(255, 255, 255, 0.9);
    font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande',
                 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    animation: fadeSlideUp 1s ease 0.3s both;
  }

  /* ── Entrance animations ── */
  @keyframes fadeSlideDown {
    from {
      opacity: 0;
      transform: translateY(-24px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes fadeSlideUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* ── Responsive ── */
  @media (max-width: 600px) {
    .title-sub {
      letter-spacing: 0.15em;
    }

    p {
      padding: 0 6vw;
    }
  }
</style>
