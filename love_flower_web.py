import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Love Flower 🌸", page_icon="💐", layout="centered")
st.title("💐 A Beautiful Flower for You 💐")

message = st.text_input("Type your message here:", "I Love You ❤️")

flower_js = f"""
<canvas id="myCanvas" width="500" height="500"></canvas>
<script>
const canvas = document.getElementById('myCanvas');
const ctx = canvas.getContext('2d');

// petals
let petals = [];
const baseColors = ['#FF4C4C', '#FF8C69', '#FFC300', '#FF69B4', '#FF1493', '#DB7093', '#FF6347', '#FFA07A'];
for(let i=0;i<40;i++){{
    petals.push({{
        angle: i*9,
        size: 40 + Math.random()*20,
        colorIndex: i % baseColors.length,
        speed: 0.2 + Math.random()*0.5,
        radius: Math.random()*20,
        sway: Math.random()*0.05
    }});
}}

// sparkles
let sparkles = [];
for(let i=0;i<60;i++){{
    sparkles.push({{
        x: Math.random()*500,
        y: Math.random()*500,
        radius: Math.random()*2 + 1,
        alpha: Math.random(),
        speedY: 0.2 + Math.random()*0.5,
        speedX: (Math.random()-0.5)*0.3
    }});
}}

function hslShift(hex, degree) {{
    let r = parseInt(hex.slice(1,3),16)/255;
    let g = parseInt(hex.slice(3,5),16)/255;
    let b = parseInt(hex.slice(5,7),16)/255;
    let max = Math.max(r,g,b), min=Math.min(r,g,b);
    let h,s,l = (max+min)/2;
    if(max==min){{ h=s=0; }}
    else {{
        let d = max-min;
        s = l>0.5?d/(2-max-min):d/(max+min);
        switch(max){{
            case r: h = (g-b)/d + (g<b?6:0); break;
            case g: h = (b-r)/d + 2; break;
            case b: h = (r-g)/d + 4; break;
        }}
        h /= 6;
    }}
    h = (h*360 + degree)%360;
    return `hsl(${{h}},${{s*100}}%,${{l*100}}%)`;
}}

let alpha = 0;
let alphaDirection = 1;
let colorShift = 0;

function draw() {{
    ctx.clearRect(0,0,500,500);

    // draw petals with color shift and sway
    petals.forEach(p => {{
        ctx.save();
        ctx.translate(250, 250);
        let swayOffset = Math.sin(p.angle*0.1)*10;
        ctx.rotate((p.angle + swayOffset) * Math.PI / 180);
        ctx.fillStyle = hslShift(baseColors[p.colorIndex], colorShift);
        ctx.beginPath();
        ctx.ellipse(p.radius + p.size, 0, 15, 50, 0, 0, 2 * Math.PI);
        ctx.fill();
        ctx.restore();

        p.angle += p.speed;
        p.radius += 0.05; // gentle outward movement
        if(p.radius > 40){{
            p.radius = 0; // reset to center for continuous flow
        }}
    }});

    // draw glowing heart
    ctx.save();
    ctx.translate(250, 250);
    let gradient = ctx.createRadialGradient(0,0,10,0,0,60);
    gradient.addColorStop(0, 'rgba(255,0,0,1)');
    gradient.addColorStop(1, 'rgba(255,105,180,0.2)');
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.moveTo(0, -20);
    ctx.bezierCurveTo(25, -50, 75, -25, 0, 50);
    ctx.bezierCurveTo(-75, -25, -25, -50, 0, -20);
    ctx.fill();
    ctx.restore();

    // draw sparkles
    sparkles.forEach(s => {{
        ctx.save();
        ctx.globalAlpha = s.alpha;
        ctx.fillStyle = 'white';
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.radius, 0, 2*Math.PI);
        ctx.fill();
        ctx.restore();

        s.y -= s.speedY;
        s.x += s.speedX;
        s.alpha += (Math.random()-0.5)*0.02;
        if(s.alpha > 1) s.alpha = 1;
        if(s.alpha < 0) s.alpha = 0;
        if(s.y < 0) s.y = 500;
        if(s.x < 0) s.x = 500;
        if(s.x > 500) s.x = 0;
    }});

    // draw pulsing message
    ctx.save();
    ctx.translate(250, 250);
    ctx.font = "24px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    alpha += 0.02 * alphaDirection;
    if(alpha > 1){{ alpha = 1; alphaDirection = -1; }}
    if(alpha < 0){{ alpha = 0; alphaDirection = 1; }}
    ctx.fillStyle = `rgba(255,0,0,${{alpha}})`;
    ctx.fillText("{message}", 0, 0);
    ctx.restore();

    colorShift += 1;
    requestAnimationFrame(draw);
}}

draw();
</script>
"""

components.html(flower_js, height=520)

