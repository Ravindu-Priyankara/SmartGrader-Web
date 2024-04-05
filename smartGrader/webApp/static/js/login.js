
let tl = gsap.timeline({});

tl.from(".gsap-logo", {duration: 0.7,
  y: -100,
  opacity: 0,
})
  .from(
    ".heading-login",
    {
      x: -40,
      opacity: 0,
    },
    "-=0.3"
  )
  .from(".input", {
    opacity: 0,
    duration: 0.5,
    stagger: 0.25,
  })
  .from(
    ".submit-button",
    {
      y: 40,
      opacity: 0,
    },
    "-=0.5"
  );