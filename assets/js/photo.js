/**
 * Photo measure tool.
 *
 * Deliberately local: the image is read with FileReader and drawn to a canvas.
 * Nothing is uploaded, which is both a privacy statement and the only option on
 * a static host. Scale comes from a known-length reference the user marks first.
 */
(function () {
  'use strict';

  var root = document.getElementById('photo');
  if (!root) return;

  var i18n;
  try { i18n = JSON.parse(root.getAttribute('data-i18n') || '{}'); } catch (e) { i18n = {}; }

  if (!window.FileReader || !document.createElement('canvas').getContext) {
    root.innerHTML = '';
    root.appendChild(p('photo__hint', i18n.noSupport || 'This browser cannot run the photo tool.'));
    return;
  }

  var image = null;
  var scale = 0;            // pixels per millimetre
  var points = [];          // up to 2 points for the reference, then up to 2 for the measurement
  var mode = 'reference';   // 'reference' | 'measure'
  var canvas = document.createElement('canvas');
  var ctx = canvas.getContext('2d');

  function p(cls, text) {
    var node = document.createElement('p');
    if (cls) node.className = cls;
    node.textContent = text;
    return node;
  }

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function build() {
    root.innerHTML = '';
    root.appendChild(p('wizard__progress', i18n.title));
    root.appendChild(p('photo__hint', i18n.hint));

    var drop = el('label', 'photo__drop');
    drop.appendChild(el('span', null, i18n.drop));
    var input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.addEventListener('change', function (event) {
      var file = event.target.files && event.target.files[0];
      if (file) load(file);
    });
    drop.appendChild(input);
    root.appendChild(drop);

    var stage = el('div', 'photo__stage');
    stage.appendChild(canvas);
    stage.style.display = 'none';
    root.appendChild(stage);
    root._stage = stage;

    var step1 = el('p', 'photo__step', i18n.setReference);
    root.appendChild(step1);

    var controls = el('div', 'photo__controls');
    var label = el('label', null, i18n.referenceLength);
    var refInput = document.createElement('input');
    refInput.type = 'number';
    refInput.min = '1';
    refInput.step = '0.01';
    refInput.value = '85.6';
    controls.appendChild(label);
    controls.appendChild(refInput);

    var step2 = el('p', 'photo__step', i18n.measure);
    root.appendChild(step2);

    var out = el('div', 'photo__out', '—');
    controls.appendChild(out);
    root.appendChild(controls);

    var buttons = el('div', 'wizard__nav');
    var modeBtn = el('button', 'wizard__btn wizard__btn--primary', i18n.measure);
    modeBtn.type = 'button';
    modeBtn.addEventListener('click', function () {
      if (!scale) return;
      mode = 'measure';
      points = [];
      draw();
      out.textContent = '—';
    });
    var resetBtn = el('button', 'wizard__btn', i18n.reset);
    resetBtn.type = 'button';
    resetBtn.addEventListener('click', function () {
      scale = 0; mode = 'reference'; points = [];
      out.textContent = '—';
      draw();
    });
    buttons.appendChild(modeBtn);
    buttons.appendChild(resetBtn);
    root.appendChild(buttons);

    root._refInput = refInput;
    root._out = out;

    canvas.addEventListener('click', onClick);
    canvas.addEventListener('touchend', function (event) {
      if (!event.changedTouches.length) return;
      event.preventDefault();
      var touch = event.changedTouches[0];
      handlePoint(touch.clientX, touch.clientY);
    }, { passive: false });
  }

  function load(file) {
    var reader = new FileReader();
    reader.onload = function (event) {
      var img = new Image();
      img.onload = function () {
        image = img;
        var maxW = Math.min(root.clientWidth - 2 || 640, 900);
        var ratio = Math.min(1, maxW / img.width);
        canvas.width = Math.round(img.width * ratio);
        canvas.height = Math.round(img.height * ratio);
        scale = 0; mode = 'reference'; points = [];
        root._stage.style.display = 'block';
        root._out.textContent = '—';
        draw();
      };
      img.src = event.target.result;
    };
    reader.readAsDataURL(file);
  }

  function toCanvasXY(clientX, clientY) {
    var rect = canvas.getBoundingClientRect();
    return {
      x: (clientX - rect.left) * (canvas.width / rect.width),
      y: (clientY - rect.top) * (canvas.height / rect.height)
    };
  }

  function onClick(event) {
    handlePoint(event.clientX, event.clientY);
  }

  function handlePoint(clientX, clientY) {
    if (!image) return;
    points.push(toCanvasXY(clientX, clientY));
    if (points.length === 2) {
      var d = distance(points[0], points[1]);
      if (mode === 'reference') {
        var mm = parseFloat(root._refInput.value);
        if (mm > 0 && d > 0) {
          scale = d / mm;
          mode = 'measure';
          points = [];
        }
      } else {
        root._out.textContent = (d / scale).toFixed(1) + ' mm';
        points = [];
      }
    }
    draw();
  }

  function distance(a, b) {
    return Math.sqrt(Math.pow(a.x - b.x, 2) + Math.pow(a.y - b.y, 2));
  }

  function draw() {
    if (!image) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(image, 0, 0, canvas.width, canvas.height);

    if (points.length === 1) {
      ctx.fillStyle = '#0b5fff';
      ctx.beginPath();
      ctx.arc(points[0].x, points[0].y, 5, 0, Math.PI * 2);
      ctx.fill();
    }
    if (points.length === 2) {
      ctx.strokeStyle = '#0b5fff';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(points[0].x, points[0].y);
      ctx.lineTo(points[1].x, points[1].y);
      ctx.stroke();
    }

    if (!scale) {
      ctx.fillStyle = 'rgba(0,0,0,0.55)';
      ctx.fillRect(0, 0, canvas.width, 34);
      ctx.fillStyle = '#fff';
      ctx.font = '15px system-ui, sans-serif';
      ctx.fillText(i18n.setReference || 'Mark the known object', 10, 23);
    }
  }

  build();
})();
