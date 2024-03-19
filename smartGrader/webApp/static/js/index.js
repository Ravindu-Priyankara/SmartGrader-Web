/*
    This function initializes Locomotive Scroll, a smooth scrolling library,
    and configures various scroll-triggered animations and effects.

    It registers Locomotive Scroll as the scroll trigger for animations.
    It also handles the scrolling of images and pins sections of the page based on scroll position.

    Additionally, it toggles a class on the footer to show or hide it based on scroll direction.

    Author: Ravindu Priyankara 03/10/2024
*/


function locomotive() {
    // Register ScrollTrigger plugin from GSAP
    gsap.registerPlugin(ScrollTrigger);
  
    // Initialize Locomotive Scroll
    const locoScroll = new LocomotiveScroll({
      el: document.querySelector("#main"),// Scroll container
      smooth: true ,// Enable smooth scrolling
    });
  
    // Update ScrollTrigger when Locomotive Scroll scrolls
    locoScroll.on("scroll", ScrollTrigger.update);
  
    // Proxy scroll events to Locomotive Scroll
    ScrollTrigger.scrollerProxy("#main", {
      scrollTop(value) {
        return arguments.length
          ? locoScroll.scrollTo(value, 0, 0)
          : locoScroll.scroll.instance.scroll.y;
      },
  
      getBoundingClientRect() {
        return {
          top: 0,
          left: 0,
          width: window.innerWidth,
          height: window.innerHeight,
        };
      },
  
      // Determine pinType based on transform support
      pinType: document.querySelector("#main").style.transform
        ? "transform"
        : "fixed",
    });
  
    // Update Locomotive Scroll on ScrollTrigger refresh
    ScrollTrigger.addEventListener("refresh", () => locoScroll.update());
    ScrollTrigger.refresh();
  }
  
  // Call locomotive function to initialize Locomotive Scroll
  locomotive();
  
  const canvas = document.querySelector("canvas");
  const context = canvas.getContext("2d");
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  
  
  window.addEventListener("resize", function () {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    render();
  });
    
    function files(index) {
      var data = `
         /static/3d-model/0001.png
         /static/3d-model/0002.png
         /static/3d-model/0003.png
         /static/3d-model/0004.png
         /static/3d-model/0005.png
         /static/3d-model/0006.png
         /static/3d-model/0007.png
         /static/3d-model/0008.png
         /static/3d-model/0009.png
         /static/3d-model/0010.png
         /static/3d-model/0011.png
         /static/3d-model/0012.png
         /static/3d-model/0013.png
         /static/3d-model/0014.png
         /static/3d-model/0015.png
         /static/3d-model/0016.png
         /static/3d-model/0017.png
         /static/3d-model/0018.png
         /static/3d-model/0019.png
         /static/3d-model/0020.png
         /static/3d-model/0021.png
         /static/3d-model/0022.png
         /static/3d-model/0023.png
         /static/3d-model/0024.png
         /static/3d-model/0025.png
         /static/3d-model/0026.png
         /static/3d-model/0027.png
         /static/3d-model/0028.png
         /static/3d-model/0029.png
         /static/3d-model/0030.png
         /static/3d-model/0031.png
         /static/3d-model/0032.png
         /static/3d-model/0033.png
         /static/3d-model/0034.png
         /static/3d-model/0035.png
         /static/3d-model/0036.png
         /static/3d-model/0037.png
         /static/3d-model/0038.png
         /static/3d-model/0039.png
         /static/3d-model/0040.png
         /static/3d-model/0041.png
         /static/3d-model/0042.png
         /static/3d-model/0043.png
         /static/3d-model/0044.png
         /static/3d-model/0045.png
         /static/3d-model/0046.png
         /static/3d-model/0047.png
         /static/3d-model/0048.png
         /static/3d-model/0049.png
         /static/3d-model/0050.png
         /static/3d-model/0051.png
         /static/3d-model/0052.png
         /static/3d-model/0053.png
         /static/3d-model/0054.png
         /static/3d-model/0055.png
         /static/3d-model/0056.png
         /static/3d-model/0057.png
         /static/3d-model/0058.png
         /static/3d-model/0059.png
         /static/3d-model/0060.png
         /static/3d-model/0061.png
         /static/3d-model/0062.png
         /static/3d-model/0063.png
         /static/3d-model/0064.png
         /static/3d-model/0065.png
         /static/3d-model/0066.png
         /static/3d-model/0067.png
         /static/3d-model/0068.png
         /static/3d-model/0069.png
         /static/3d-model/0070.png
         /static/3d-model/0071.png
         /static/3d-model/0072.png
         /static/3d-model/0073.png
         /static/3d-model/0074.png
         /static/3d-model/0075.png
         /static/3d-model/0076.png
         /static/3d-model/0077.png
         /static/3d-model/0078.png
         /static/3d-model/0079.png
         /static/3d-model/0080.png
         /static/3d-model/0081.png
         /static/3d-model/0082.png
         /static/3d-model/0083.png
         /static/3d-model/0084.png
         /static/3d-model/0085.png
         /static/3d-model/0086.png
         /static/3d-model/0087.png
         /static/3d-model/0088.png
         /static/3d-model/0089.png
         /static/3d-model/0090.png
         /static/3d-model/0091.png
         /static/3d-model/0092.png
         /static/3d-model/0093.png
         /static/3d-model/0094.png
         /static/3d-model/0095.png
         /static/3d-model/0096.png
         /static/3d-model/0097.png
         /static/3d-model/0098.png
         /static/3d-model/0099.png
         /static/3d-model/0100.png
         /static/3d-model/0101.png
         /static/3d-model/0102.png
         /static/3d-model/0103.png
         /static/3d-model/0104.png
         /static/3d-model/0105.png
         /static/3d-model/0106.png
         /static/3d-model/0107.png
         /static/3d-model/0108.png
         /static/3d-model/0109.png
         /static/3d-model/0110.png
         /static/3d-model/0111.png
         /static/3d-model/0112.png
         /static/3d-model/0113.png
         /static/3d-model/0114.png
         /static/3d-model/0115.png
         /static/3d-model/0116.png
         /static/3d-model/0117.png
         /static/3d-model/0118.png
         /static/3d-model/0119.png
         /static/3d-model/0120.png
         /static/3d-model/0121.png
         /static/3d-model/0122.png
         /static/3d-model/0123.png
         /static/3d-model/0124.png
         /static/3d-model/0125.png
         /static/3d-model/0126.png
         /static/3d-model/0127.png
         /static/3d-model/0128.png
         /static/3d-model/0129.png
         /static/3d-model/0130.png
         /static/3d-model/0131.png
         /static/3d-model/0132.png
         /static/3d-model/0133.png
         /static/3d-model/0134.png
         /static/3d-model/0135.png
         /static/3d-model/0136.png
         /static/3d-model/0137.png
         /static/3d-model/0138.png
         /static/3d-model/0139.png
         /static/3d-model/0140.png
         /static/3d-model/0141.png
         /static/3d-model/0142.png
         /static/3d-model/0143.png
         /static/3d-model/0144.png
         /static/3d-model/0145.png
         /static/3d-model/0146.png
         /static/3d-model/0147.png
         /static/3d-model/0148.png
         /static/3d-model/0149.png
         /static/3d-model/0150.png
         /static/3d-model/0151.png
         /static/3d-model/0152.png
         /static/3d-model/0153.png
         /static/3d-model/0154.png
         /static/3d-model/0155.png
         /static/3d-model/0156.png
         /static/3d-model/0157.png
         /static/3d-model/0158.png
         /static/3d-model/0159.png
         /static/3d-model/0160.png
         /static/3d-model/0161.png
         /static/3d-model/0162.png
         /static/3d-model/0163.png
         /static/3d-model/0164.png
         /static/3d-model/0165.png
         /static/3d-model/0166.png
         /static/3d-model/0167.png
         /static/3d-model/0168.png
         /static/3d-model/0169.png
         /static/3d-model/0170.png
         /static/3d-model/0171.png
         /static/3d-model/0172.png
         /static/3d-model/0173.png
         /static/3d-model/0174.png
         /static/3d-model/0175.png
         /static/3d-model/0176.png
         /static/3d-model/0177.png
         /static/3d-model/0178.png
         /static/3d-model/0179.png
         /static/3d-model/0180.png
         /static/3d-model/0181.png
         /static/3d-model/0182.png
         /static/3d-model/0183.png
         /static/3d-model/0184.png
         /static/3d-model/0185.png
         /static/3d-model/0186.png
         /static/3d-model/0187.png
         /static/3d-model/0188.png
         /static/3d-model/0189.png
         /static/3d-model/0190.png
         /static/3d-model/0191.png
         /static/3d-model/0192.png
         /static/3d-model/0193.png
         /static/3d-model/0194.png
         /static/3d-model/0195.png
         /static/3d-model/0196.png
         /static/3d-model/0197.png
         /static/3d-model/0198.png
         /static/3d-model/0199.png
         /static/3d-model/0200.png
         /static/3d-model/0201.png
         /static/3d-model/0202.png
         /static/3d-model/0203.png
         /static/3d-model/0204.png
         /static/3d-model/0205.png
         /static/3d-model/0206.png
         /static/3d-model/0207.png
         /static/3d-model/0208.png
         /static/3d-model/0209.png
         /static/3d-model/0210.png
         /static/3d-model/0211.png
         /static/3d-model/0212.png
         /static/3d-model/0213.png
         /static/3d-model/0214.png
         /static/3d-model/0215.png
         /static/3d-model/0216.png
         /static/3d-model/0217.png
         /static/3d-model/0218.png
         /static/3d-model/0219.png
         /static/3d-model/0220.png
         /static/3d-model/0221.png
         /static/3d-model/0222.png
         /static/3d-model/0223.png
         /static/3d-model/0224.png
         /static/3d-model/0225.png
         /static/3d-model/0226.png
         /static/3d-model/0227.png
         /static/3d-model/0228.png
         /static/3d-model/0229.png
         /static/3d-model/0230.png
         /static/3d-model/0231.png
         /static/3d-model/0232.png
         /static/3d-model/0233.png
         /static/3d-model/0234.png
         /static/3d-model/0235.png
         /static/3d-model/0236.png
         /static/3d-model/0237.png
         /static/3d-model/0238.png
         /static/3d-model/0239.png
         /static/3d-model/0240.png
         /static/3d-model/0241.png
         /static/3d-model/0242.png
         /static/3d-model/0243.png
         /static/3d-model/0244.png
         /static/3d-model/0245.png
         /static/3d-model/0246.png
         /static/3d-model/0247.png
         /static/3d-model/0248.png
         /static/3d-model/0249.png
         /static/3d-model/0250.png
         /static/3d-model/0251.png
         /static/3d-model/0252.png
         /static/3d-model/0253.png
         /static/3d-model/0254.png
         /static/3d-model/0255.png
         /static/3d-model/0256.png
         /static/3d-model/0257.png
         /static/3d-model/0258.png
         /static/3d-model/0259.png
         /static/3d-model/0260.png
         /static/3d-model/0261.png
         /static/3d-model/0262.png
         /static/3d-model/0263.png
         /static/3d-model/0264.png
         /static/3d-model/0265.png
         /static/3d-model/0266.png
         /static/3d-model/0267.png
         /static/3d-model/0268.png
         /static/3d-model/0269.png
         /static/3d-model/0270.png
         /static/3d-model/0271.png
         /static/3d-model/0272.png
         /static/3d-model/0273.png
         /static/3d-model/0274.png
         /static/3d-model/0275.png
         /static/3d-model/0276.png
         /static/3d-model/0277.png
         /static/3d-model/0278.png
         /static/3d-model/0279.png
         /static/3d-model/0280.png
         /static/3d-model/0281.png
         /static/3d-model/0282.png
         /static/3d-model/0283.png
         /static/3d-model/0284.png
         /static/3d-model/0285.png
         /static/3d-model/0286.png
         /static/3d-model/0287.png
         /static/3d-model/0288.png
         /static/3d-model/0289.png
         /static/3d-model/0290.png
         /static/3d-model/0291.png
         /static/3d-model/0292.png
         /static/3d-model/0293.png
         /static/3d-model/0294.png
         /static/3d-model/0295.png
         /static/3d-model/0296.png
         /static/3d-model/0297.png
         /static/3d-model/0298.png
         /static/3d-model/0299.png
         /static/model/0300.png
     `;
      return data.split("\n")[index];
    }
    
  // Load images for animation sequence
  const frameCount = 300;
  
  const images = [];
  const imageSeq = {
    frame: 1,
  };
  
  // Populate images array with image objects
  for (let i = 0; i < frameCount; i++) {
    const img = new Image();
    img.src = files(i);
    images.push(img);
  }
  
  // Configure animation sequence using GSAP and ScrollTrigger
  gsap.to(imageSeq, {
    frame: frameCount - 1,
    snap: "frame",
    ease: `none`,
    scrollTrigger: {
      scrub: 0.15,
      trigger: `#page>canvas`,
      start: `top top`,
      end: `600% top`,
      scroller: `#main`,
    },
    onUpdate: render,
  });
  
  // Update render function on image load
  images[1].onload = render;
  
  // Render function to scale and draw images on canvas
  function render() {
    scaleImage(images[imageSeq.frame], context);
  }
  
  // Function to scale and draw images on canvas
  function scaleImage(img, ctx) {
    // Scaling and positioning calculations
    var canvas = ctx.canvas;
    var hRatio = canvas.width / img.width;
    var vRatio = canvas.height / img.height;
    var ratio = Math.max(hRatio, vRatio);
    var centerShift_x = (canvas.width - img.width * ratio) / 2;
    var centerShift_y = (canvas.height - img.height * ratio) / 2;
  
    // Clear canvas and draw scaled image
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(
      img,
      0,
      0,
      img.width,
      img.height,
      centerShift_x,
      centerShift_y,
      img.width * ratio,
      img.height * ratio
    );
  }
  ScrollTrigger.create({
    trigger: "#page>canvas",
    pin: true,
    // markers:true,
    scroller: `#main`,
    start: `top top`,
    end: `600% top`,
  });
  
  // Pin sections of the page based on scroll position
  gsap.to("#page1",{
    scrollTrigger:{
      trigger:`#page1`,
      start:`top top`,
      end:`bottom top`,
      pin:true,
      scroller:`#main`
    }
  })
  gsap.to("#page2",{
    scrollTrigger:{
      trigger:`#page2`,
      start:`top top`,
      end:`bottom top`,
      pin:true,
      scroller:`#main`
    }
  })
  gsap.to("#page3",{
    scrollTrigger:{
      trigger:`#page3`,
      start:`top top`,
      end:`bottom top`,
      pin:true,
      scroller:`#main`
    }
  })
  
  // Toggle footer visibility based on scroll direction
  ScrollTrigger.create({
    trigger: "footer",
    start: "top bottom",
    end: "bottom top",
    toggleClass: {className: "hide-footer", targets: "footer"},
    scroller: "#main",
  });
  
  /** 
   * 
   * I'm not using below functions these are use to disable and enable locomotive scroll.
   * 
  **/
  
  
  // Function to disable Locomotive Scroll
  function disableLocomotiveScroll() {
    // Remove event listeners or destroy Locomotive Scroll instance
    locoScroll.destroy();
  }
  
  // Function to enable Locomotive Scroll
  function enableLocomotiveScroll() {
    // Reinitialize Locomotive Scroll
    locomotive();
  }
  
  /** 
   * A touch of brilliance by the mastermind, Ravindu Priyankara,😜😈
   * crafting elegance in code. 
   * EOF: The end of this masterpiece. 
  **/