<script>
  export let numbers;

  let colorNames = [
    "Crimson",
    "DeepPink",
    "Coral",
    "PaleGoldenrod",
    "Magenta",
    "Chartreuse",
    "DarkOliveGreen",
    "PaleTurquoise",
    "RoyalBlue",
    "BlanchedAlmond",
    "Sienna",
    "DarkSlateGray",
    "AliceBlue",
    "Chocolate",
    "DarkBlue",
    "DarkGreen",
    "DarkSalmon",
    "DarkViolet",
    "ForestGreen",
    "Fuchsia",
    "Gold",
  ];
  let colorIterator = 0;

  function getNextColor() {
    let a = colorNames[colorIterator];
    colorIterator += 1;
    colorIterator = colorIterator % colorNames.length;
    return a;
  }

  const margin = { top: 20, right: 20, bottom: 20, left: 20 };

  let clientWidth;
  let clientHeight;

  $: width = clientWidth - (margin.left + margin.right);
  $: height = clientHeight - (margin.top + margin.bottom);

  $: bounds = {
    top: margin.top,
    left: margin.left,
    bottom: margin.top + height,
    right: margin.left + width,
  };

  function deepCopy(x) {
    let s = JSON.stringify(x);
    let theCopy = JSON.parse(s);
    return theCopy;
  }

  function markup(population, minX, maxX, level) {
    population.minX = minX;
    population.maxX = maxX;
    population.level = level;
    population.color = getNextColor();
    if (population.data) {
      if (typeof population.data != "number") {
        let childWidth = (maxX - minX) / population.data.length;
        for (let i = 0; i < population.data.length; ++i) {
          markup(
            population.data[i],
            minX + i * childWidth,
            minX + (i + 1) * childWidth,
            level + 1
          );
        }
      }
    }
    return population;
  }

  $: aData = markup(deepCopy(numbers), 0, 1, 0);

  $: maxValue = findMaxValue(aData);

  $: levels = findLevels(aData, 0, 1);

  function findMaxValue(population) {
    if (typeof population.data == "number") {
      return population.data;
    }
    let maxVal = 0.0;
    if (population.data) {
      for (let i = 0; i < population.data.length; ++i) {
        let val = findMaxValue(population.data[i]);
        if (val > maxVal) {
          maxVal = val;
        }
      }
    }
    return maxVal;
  }

  function findLevels(population, minX, maxX) {
    if (!population) return 0;
    if (typeof population.data == "number") return 0;
    let maxDepth = 0;
    if (population.data) {
      for (let i = 0; i < population.data.length; ++i) {
        let childDepth = findLevels(population.data[i]);
        if (childDepth > maxDepth) maxDepth = childDepth;
      }
    }
    return maxDepth + 1;
  }

  function getLabel(population) {
    return `${population.label} ${population.minX} ${population.maxX} ${population.level}`;
  }

  function findPopulations(population) {
    let a = [];
    if (!population) return a;
    if (population.data) {
      if (typeof population.data != "number") {
        a = population.data.map((pop) => findPopulations(pop));
      }
      a.push(population);
    }
    return a.flat();
  }

  function findLabels2(population) {
    return findPopulations(population).map((pop) => getLabel(pop));
  }

  function populationsAtLevel(population, n) {
    return findPopulations(population).filter((pop) => pop.level == n);
  }
</script>

<h3>
  {numbers.dx}
</h3>

<div
  class="sizer"
  bind:clientWidth
  bind:clientHeight
  height="60vh"
  width="90vw"
>
  {#if clientWidth && numbers}
    <svg width="100%" height="60vh">
      <g transform={`translate(${margin.left}, ${bounds.bottom})`}>
        <g transform="scale(1, -1)">
          {#if height > 20}
            {#each populationsAtLevel(aData, levels) as pop}
              <rect
                x={width * pop.minX + 0.05 * (pop.maxX - pop.minX)}
                width={width * 0.9 * (pop.maxX - pop.minX)}
                y={20 * (levels + 1)}
                height={((height - 20 * (levels + 1)) * pop.data) / maxValue}
                fill={pop.color}
              />
            {/each}
          {/if}
        </g>
        {#each findPopulations(aData) as pop}
          {#if pop.level < levels}
            <line
              x1={width * pop.minX + 14}
              x2={width * pop.maxX - 28}
              y1={20 * -pop.level}
              y2={20 * -pop.level}
              stroke="black"
            />
            <line
              x1={width * pop.minX + 14}
              x2={width * pop.minX + 14}
              y1={20 * -pop.level}
              y2={20 * -pop.level - 5}
              stroke="black"
            />
            <line
              x1={width * pop.maxX - 28}
              x2={width * pop.maxX - 28}
              y1={20 * -pop.level}
              y2={20 * -pop.level - 5}
              stroke="black"
            />
          {/if}
          <text
            x={(width * (pop.maxX + pop.minX)) / 2}
            y={20 * -pop.level - 2}
            text-anchor="middle"
          >
            {pop.label}
          </text>
        {/each}
      </g>
    </svg>
  {/if}
</div>

<style>
  h3 {
    margin: auto;
    text-align: center;
  }
  svg {
    /* Note that both of these must be set to keep the graphic from going over the
      top menu banner: */
    position: relative;
    z-index: -1;
  }
</style>
