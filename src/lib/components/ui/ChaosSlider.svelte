<script lang="ts">
  interface Props {
    value: number;
    onchange?: (value: number) => void;
  }

  let { value = $bindable(), onchange }: Props = $props();

  function handleChange(e: Event) {
    const target = e.target as HTMLInputElement;
    value = parseInt(target.value);
    onchange?.(value);
  }

  const chaosDescriptions: Record<number, string> = {
    1: 'Very safe, like milk',
    2: 'Slightly risky',
    3: 'Normal weird',
    4: 'Getting spicy',
    5: 'Ralph default',
    6: 'Pretty chaotic',
    7: 'Maximum weird',
    8: 'Brain melting',
    9: 'Leprechaun mode',
    10: 'PURE CHAOS'
  };

  const chaosEmojis: Record<number, string> = {
    1: '🥛',
    2: '🌱',
    3: '🎭',
    4: '🌶️',
    5: '🧒',
    6: '🎪',
    7: '🌀',
    8: '🧠',
    9: '🍀',
    10: '💥'
  };
</script>

<div class="chaos-slider">
  <div class="flex justify-between items-center mb-2">
    <label for="chaos-slider" class="font-chalk text-chalkboard">Chaos Level</label>
    <span class="text-2xl">{chaosEmojis[value]}</span>
  </div>

  <input
    type="range"
    id="chaos-slider"
    min="1"
    max="10"
    {value}
    oninput={handleChange}
    class="w-full h-4 rounded-full appearance-none cursor-pointer
           bg-gradient-to-r from-playground-green via-ralph-yellow to-playground-red
           border-2 border-chalkboard"
    style="--thumb-size: 24px;"
  />

  <div class="flex justify-between text-xs text-chalkboard/60 mt-1">
    <span>Safe</span>
    <span class="font-chalk text-sm text-chalkboard">{value}/10</span>
    <span>Chaos</span>
  </div>

  <p class="ralph-voice text-center text-sm text-chalkboard/80 mt-2">
    "{chaosDescriptions[value]}"
  </p>
</div>

<style>
  input[type='range']::-webkit-slider-thumb {
    appearance: none;
    width: var(--thumb-size);
    height: var(--thumb-size);
    background: #ffd93d;
    border: 3px solid #2d3436;
    border-radius: 50%;
    cursor: pointer;
    transition: transform 0.2s;
  }

  input[type='range']::-webkit-slider-thumb:hover {
    transform: scale(1.2);
  }

  input[type='range']::-moz-range-thumb {
    width: var(--thumb-size);
    height: var(--thumb-size);
    background: #ffd93d;
    border: 3px solid #2d3436;
    border-radius: 50%;
    cursor: pointer;
  }
</style>
