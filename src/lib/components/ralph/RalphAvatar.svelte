<script lang="ts">
  interface Props {
    size?: 'sm' | 'md' | 'lg' | 'xl';
    mood?: 'neutral' | 'thinking' | 'excited' | 'confused';
    animated?: boolean;
  }

  let { size = 'md', mood = 'neutral', animated = true }: Props = $props();

  const sizeClasses = {
    sm: 'w-12 h-12 text-2xl',
    md: 'w-24 h-24 text-4xl',
    lg: 'w-32 h-32 text-5xl',
    xl: 'w-48 h-48 text-6xl'
  };

  const moodEmojis = {
    neutral: '🧒',
    thinking: '🤔',
    excited: '🤩',
    confused: '😵'
  };

  const animationClasses = {
    neutral: 'animate-float',
    thinking: 'animate-think',
    excited: 'animate-wiggle',
    confused: 'animate-spin-slow'
  };
</script>

<div
  class="ralph-avatar {sizeClasses[size]} bg-ralph-yellow rounded-full
         border-4 border-chalkboard shadow-crayon
         flex items-center justify-center
         {animated ? animationClasses[mood] : ''}"
>
  <span>{moodEmojis[mood]}</span>
</div>

<style>
  @keyframes spin-slow {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }

  .animate-spin-slow {
    animation: spin-slow 3s linear infinite;
  }
</style>
