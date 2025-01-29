<script>
  export let numbers;
  export let horizontal = false;

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

  const margin = { top: 20, right: 100, bottom: 20, left: 100 };

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

  function populationsAtLevel(population, n) {
    return findPopulations(population).filter((pop) => pop.level == n);
  }

  function longestStringAtLevel(population, n) {
    let winner = "";
    let pops = populationsAtLevel(population, n);
    for (let i = 0; i < pops.length; ++i) {
      if (pops[i].label.length > winner.length) {
        winner = pops[i].label;
      }
    }
    return winner;
  }

  $: longestLevel_1 = longestStringAtLevel(aData, 1);
  $: longestLevel_2 = longestStringAtLevel(aData, 2);
  $: longestLevel_3 = longestStringAtLevel(aData, 3);
  $: longestLevel_4 = longestStringAtLevel(aData, 4);

  let strSizer_1;
  let strSizer_2;
  let strSizer_3;
  let strSizer_4;

  $: bb_1 = strSizer_1?.getBBox();
  $: bb_2 = strSizer_2?.getBBox();
  $: bb_3 = strSizer_3?.getBBox();
  $: bb_4 = strSizer_4?.getBBox();

  function barX(pop) {
    if (horizontal) {
      return labelAreaWidth;
    } else {
      return width * pop.minX + 0.05 * (pop.maxX - pop.minX);
    }
  }

  function barWidth(pop) {
    if (horizontal) {
      return ((width - 20 * (levels + 1)) * pop.data) / maxValue;
    } else {
      return width * 0.9 * (pop.maxX - pop.minX);
    }
  }

  function barY(pop) {
    if (horizontal) {
      return height * pop.minX + 0.05 * (pop.maxX - pop.minX);
    } else {
      return 20 * (levels + 1);
    }
  }

  function barHeight(pop) {
    if (horizontal) {
      return height * 0.9 * (pop.maxX - pop.minX);
    } else {
      return ((height - 20 * (levels + 1)) * pop.data) / maxValue;
    }
  }

  function labelX(pop) {
    if (horizontal) {
      let total = 0;
      if (pop.level > 4) {
        total += bb_4.width;
      }
      if (pop.level > 3) {
        total += bb_3.width;
      }
      if (pop.level > 2) {
        total += bb_2.width;
      }
      if (pop.level > 1) {
        total += bb_1.width;
      }
      return total;
    } else {
      return (width * (pop.maxX + pop.minX)) / 2;
    }
  }

  function labelY(pop) {
    if (horizontal) {
      return height * pop.minX + 0.5 * height * (pop.maxX - pop.minX);
    } else {
      return 20 * -pop.level - 2;
    }
  }

  function getTranslation(theBounds, isHorizontal) {
    if (isHorizontal) {
      return `translate(${margin.left}, ${margin.bottom})`;
    } else {
      return `translate(${margin.left}, ${theBounds.bottom})`;
    }
  }

  $: translation = getTranslation(bounds, horizontal);

  function getBarTransform(isHorizontal) {
    if (isHorizontal) {
      return "scale(1, 1)";
    } else {
      return "scale(1, -1)";
    }
  }

  $: barTransform = getBarTransform(horizontal);

  function getTextAnchor(isHorizontal) {
    if (isHorizontal) {
      return "end";
    } else {
      return "middle";
    }
  }

  $: textAnchor = getTextAnchor(horizontal);

  function getLabelAreaWidth() {
    let sum = 0;
    if (bb_1 !== undefined) {
      sum += bb_1.width;
    }
    if (bb_2 !== undefined) {
      sum += bb_2.width;
    }
    if (bb_3 !== undefined) {
      sum += bb_4.width;
    }
    if (bb_4 !== undefined) {
      sum += bb_4.width;
    }
    return sum;
  }

  $: labelAreaWidth = getLabelAreaWidth(bb_1, bb_2, bb_3, bb_4);
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
      <g transform={translation}>
        <g transform={barTransform}>
          {#if height > 20}
            {#each populationsAtLevel(aData, levels) as pop}
              <rect
                x={barX(pop, horizontal)}
                width={barWidth(pop, horizontal)}
                y={barY(pop, horizontal)}
                height={barHeight(pop, horizontal)}
                fill={pop.color}
              />
            {/each}
          {/if}
        </g>
        {#each findPopulations(aData) as pop}
          {#if pop.level < levels}
            {#if horizontal && pop.level > 0}}
              <line
                x1={labelX(pop) + 4}
                x2={labelX(pop) + 4}
                y1={height * pop.minX + 14}
                y2={height * pop.maxX - 24}
                stroke="black"
              />
              <line
                x1={labelX(pop) + 4}
                x2={labelX(pop) + 14}
                y1={height * pop.minX + 14}
                y2={height * pop.minX + 14}
                stroke="black"
              />
              <line
                x1={labelX(pop) + 4}
                x2={labelX(pop) + 14}
                y1={height * pop.maxX - 24}
                y2={height * pop.maxX - 24}
                stroke="black"
              />
            {:else if !horizontal}
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
          {/if}
          {#if !horizontal || pop.level > 0}
            <text
              x={labelX(pop, horizontal)}
              y={labelY(pop, clientHeight, horizontal)}
              text-anchor={textAnchor}
            >
              {pop.label}
            </text>
          {/if}
        {/each}

        <!-- Discreetly find out the text size of our labels -->
        <text x="-1000" y="-1000" bind:this={strSizer_1}
          >m {longestLevel_1}
        </text>
        <text x="-1000" y="-1000" bind:this={strSizer_2}
          >m {longestLevel_2}
        </text>
        <text x="-1000" y="-1000" bind:this={strSizer_3}
          >m {longestLevel_3}
        </text>
        <text x="-1000" y="-1000" bind:this={strSizer_4}
          >m {longestLevel_4}
        </text>
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
