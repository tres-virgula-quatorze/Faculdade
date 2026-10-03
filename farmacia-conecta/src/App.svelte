<script>
  import Header from './lib/components/Header.svelte'
  import Hero from './lib/components/Hero.svelte'
  import Services from './lib/components/Services.svelte'
  import BookingForm from './lib/components/BookingForm.svelte'
  import About from './lib/components/About.svelte'
  import Footer from './lib/components/Footer.svelte'
</script>

<Header />
<main id="main-content">
  <Hero />
  <Services />
  <BookingForm />
  <About />
</main>
<Footer />

<style>
  #main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    width: 100%;
  }
</style>
