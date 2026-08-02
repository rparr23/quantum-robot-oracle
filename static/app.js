const form = document.querySelector('#oracle-form');
const runButton = document.querySelector('#run');
const errorBox = document.querySelector('#error');
const speakButton = document.querySelector('#speak');
let lastAnswer = '';

function setResult(data) {
  document.querySelector('#empty').hidden = true;
  document.querySelector('#results').hidden = false;
  document.querySelector('#answer').textContent = data.answer;
  document.querySelector('#shot-label').textContent = `${data.shots} SHOTS`;
  document.querySelector('#circuit-text').textContent = data.circuit;
  ['0', '1'].forEach((state) => {
    const percentage = data.probabilities[state] * 100;
    document.querySelector(`#bar-${state}`).style.width = `${percentage}%`;
    document.querySelector(`#prob-${state}`).textContent = `${percentage.toFixed(1)}%`;
    document.querySelector(`#count-${state}`).textContent = `${data.counts[state]} / ${data.shots}`;
  });
  lastAnswer = data.answer;
  speakButton.disabled = !window.VECTOR_ENABLED;
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  errorBox.hidden = true;
  runButton.disabled = true;
  runButton.innerHTML = '<span class="spinner"></span> Measuring…';
  try {
    const response = await fetch('/api/oracle', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({question: form.question.value, shots: Number(form.shots.value)})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'The experiment could not run.');
    setResult(data);
  } catch (error) {
    errorBox.textContent = error.message;
    errorBox.hidden = false;
  } finally {
    runButton.disabled = false;
    runButton.innerHTML = '<span aria-hidden="true">▶</span> Run again';
  }
});

speakButton.addEventListener('click', async () => {
  speakButton.disabled = true;
  const response = await fetch('/api/vector/speak', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({text: `The quantum oracle says ${lastAnswer}`})
  });
  const data = await response.json();
  if (!response.ok) {
    errorBox.textContent = data.error;
    errorBox.hidden = false;
  }
  speakButton.disabled = false;
});

