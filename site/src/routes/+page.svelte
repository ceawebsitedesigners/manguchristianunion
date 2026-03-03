<script>
  import Home from '../lib/components/home.svelte';
	import About from '../lib/components/about.svelte';
	import Content from '../lib/components/content.svelte';
	import Events from '../lib/components/events.svelte';
	import Leadership from '../lib/components/leadership.svelte';
	import Ministries from '../lib/components/ministries.svelte';
	import Services from '../lib/components/services.svelte';
	import ContactsAndDirections from '../lib/components/contacts_and_directions.svelte';
  import Nav from '../lib/components/navbar.svelte';
</script>

<Nav />
<Home />
<About />
<Services />
<Ministries />
<Leadership />
<Events />
<ContactsAndDirections />


<style>
  /* remove global padding and margins for full fit using 100 vw and 100 vh with no overflow */
    :global(*, *::before, *::after) {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    overflow-x: hidden;
  }
</style>