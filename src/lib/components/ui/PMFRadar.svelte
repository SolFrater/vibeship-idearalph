<script lang="ts">
  import type { PMFScores } from '$lib/ralph/types';

  interface Props {
    scores: PMFScores;
    size?: number;
  }

  let { scores, size = 200 }: Props = $props();

  const labels = [
    { key: 'marketSize', label: 'Market', emoji: '🎯' },
    { key: 'problemSeverity', label: 'Problem', emoji: '🔥' },
    { key: 'solutionFit', label: 'Solution', emoji: '🧩' },
    { key: 'competition', label: 'Moat', emoji: '🏰' },
    { key: 'vibeCodeable', label: 'Buildable', emoji: '🛠️' },
    { key: 'virality', label: 'Viral', emoji: '🚀' }
  ] as const;

  const center = size / 2;
  const maxRadius = (size / 2) * 0.8;

  // Calculate points on the radar
  function getPoint(index: number, value: number) {
    const angle = (Math.PI * 2 * index) / 6 - Math.PI / 2;
    const radius = (value / 10) * maxRadius;
    return {
      x: center + Math.cos(angle) * radius,
      y: center + Math.sin(angle) * radius
    };
  }

  // Create polygon points string
  const polygonPoints = $derived(
    labels
      .map((l, i) => {
        const point = getPoint(i, scores[l.key]);
        return `${point.x},${point.y}`;
      })
      .join(' ')
  );

  // Background grid points
  function getGridPoints(level: number) {
    return labels
      .map((_, i) => {
        const point = getPoint(i, level);
        return `${point.x},${point.y}`;
      })
      .join(' ');
  }

  const average = $derived(
    Math.round(
      (Object.values(scores).reduce((sum, val) => sum + val, 0) / 6) * 10
    ) / 10
  );
</script>

<div class="pmf-radar relative" style="width: {size}px; height: {size}px;">
  <svg width={size} height={size} class="drop-shadow-lg">
    <!-- Background grid -->
    {#each [2, 4, 6, 8, 10] as level}
      <polygon
        points={getGridPoints(level)}
        fill="none"
        stroke="#2D3436"
        stroke-width="1"
        opacity={0.2}
      />
    {/each}

    <!-- Axis lines -->
    {#each labels as _, i}
      {@const point = getPoint(i, 10)}
      <line
        x1={center}
        y1={center}
        x2={point.x}
        y2={point.y}
        stroke="#2D3436"
        stroke-width="1"
        opacity={0.3}
      />
    {/each}

    <!-- Data polygon -->
    <polygon
      points={polygonPoints}
      fill="rgba(107, 203, 119, 0.4)"
      stroke="#6BCB77"
      stroke-width="3"
      class="transition-all duration-500"
    />

    <!-- Data points -->
    {#each labels as l, i}
      {@const point = getPoint(i, scores[l.key])}
      <circle
        cx={point.x}
        cy={point.y}
        r="6"
        fill="#FFD93D"
        stroke="#2D3436"
        stroke-width="2"
        class="transition-all duration-300"
      />
    {/each}
  </svg>

  <!-- Labels around the chart -->
  {#each labels as l, i}
    {@const labelPoint = getPoint(i, 12)}
    <div
      class="absolute text-center transform -translate-x-1/2 -translate-y-1/2"
      style="left: {labelPoint.x}px; top: {labelPoint.y}px;"
    >
      <span class="text-lg">{l.emoji}</span>
      <div class="text-xs font-chalk text-chalkboard">
        {l.label}
        <span class="text-xs text-chalkboard/60">({scores[l.key]})</span>
      </div>
    </div>
  {/each}

  <!-- Center average -->
  <div
    class="absolute transform -translate-x-1/2 -translate-y-1/2 text-center"
    style="left: {center}px; top: {center}px;"
  >
    <div class="text-2xl font-chalk text-chalkboard">{average}</div>
    <div class="text-xs text-chalkboard/60">avg</div>
  </div>
</div>
