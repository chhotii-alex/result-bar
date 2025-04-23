<script>
  import { tick } from "svelte";
  import { scaleLinear } from "d3-scale";
  import { line, curveBumpX } from "d3-shape";
  export let numbers;

  let width;
  let height;

  function deepCopy(x) {
    let s = JSON.stringify(x);
    let theCopy = JSON.parse(s);
    return theCopy;
  }

  function widthPointsForPop(pop) {
    if (pop.histogram) return 5;
    return 1;
  }

  let colors = { positive: "Tomato", negative: "DodgerBlue" };

  function markup(population, minDim, maxDim, level) {
    population.minDim = minDim;
    population.maxDim = maxDim;
    population.yPlace = scaleLinear().domain([0, 1]).range([minDim, maxDim]);
    population.level = level;
    population.color = colors[population.label];
    if (population.total) {
      population.xScale = scaleLinear()
        .domain([0, population.total])
        .range([0, 1]);
      if (population.histogram) {
        let peak = findDensityPeak(population.histogram);
        population.histogramY = scaleLinear()
          .domain([0, peak])
          .range([0.8, 0.05]);
        population.slices = {
          bars: scaleLinear().domain([0, 1]).range([0.75, 1.0]),
          histogram: scaleLinear().domain([0, 1]).range([0.0, 0.75]),
        };
      } else {
        population.slices = {
          bars: scaleLinear().domain([0, 1]).range([0, 1.0]),
        };
      }
    }
    if (typeof population.data != "number") {
      let widthPoints = 0;
      for (let i = 0; i < population.data.length; ++i) {
        widthPoints += findLevels(population.data[i]);
      }
      let childWidth = (maxDim - minDim) / widthPoints;
      let pointsSoFar = 0;
      for (let i = 0; i < population.data.length; ++i) {
        markup(
          population.data[i],
          minDim + pointsSoFar * childWidth,
          minDim + (pointsSoFar + findLevels(population.data[i])) * childWidth,
          level + 1
        );
        pointsSoFar += findLevels(population.data[i]);
      }
    }
    return population;
  }

  function hasAnyHistograms(population) {
    if (!population) return false;
    if (!population.data) return false;
    if (typeof population.data == "number") {
      if (population.histogram) return true;
    } else {
      for (let i = 0; i < population.data.length; ++i) {
        if (hasAnyHistograms(population.data[i])) return true;
      }
    }
    return false;
  }

  $: aData = markup(deepCopy(numbers), 0, 1, 0);

  $: hasHistograms = hasAnyHistograms(aData);

  $: maxTotal = findMaxTotal(aData);

  $: levels = findLevels(aData);

  function findMaxTotal(population) {
    if (typeof population.data == "number") {
      if (population.total) {
        return population.total;
      }
    } else if (Array.isArray(population.data)) {
      let maxVal = 0.0;
      if (population.data) {
        for (let i = 0; i < population.data.length; ++i) {
          let val = findMaxTotal(population.data[i]);
          if (val > maxVal) {
            maxVal = val;
          }
        }
      }
      return maxVal;
    }
  }

  function findLevels(population) {
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
    if (typeof population.data != "number") {
      a = population.data.map((pop) => findPopulations(pop));
    }
    if (!population.isLeaf) {
      a.push(population);
    }
    return a.flat(Infinity);
  }

  function populationsAtLevel(population, n) {
    return findPopulations(population).filter((pop) => pop.level == n);
  }

  function populationsWithGroupTotals(population) {
    return findPopulations(population).filter((pop) => pop.showTotal);
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

  function longestStringsAtLevels(population) {
    let strings = [];
    for (let i = 0; i <= findLevels(population); ++i) {
      strings.push(longestStringAtLevel(population, i));
    }
    return strings;
  }

  $: longestStrings = longestStringsAtLevels(aData);

  let stringSizeWidgetArray = Array(50).fill(null);
  let bboxArray = [];
  let strSizer_total;
  let bb_total;
  let labelAreaWidth = 0;
  let total_nums_width = 0;

  function updateSizes() {
    tick().then(() => {
      bboxArray = [];
      for (let strSizer of stringSizeWidgetArray) {
        if (strSizer) {
          bboxArray.push(strSizer.getBBox());
        }
      }
      bb_total = strSizer_total?.getBBox();
      labelAreaWidth = getLabelAreaWidth();
      total_nums_width = bb_total ? bb_total.width : 0;
    });
  }

  $: updateSizes(longestStrings);

  function getLabelAreaWidth() {
    let sum = 0;
    for (let box of bboxArray) {
      if (box) {
        sum += box.width;
      }
    }
    return sum;
  }

  function findDensityPeak(histogram) {
    let peak = 0;
    for (let bin of histogram) {
      if (bin.count > peak) {
        peak = bin.count;
      }
    }
    return peak;
  }

  $: histogramX = scaleLinear()
    .domain([0, 10])
    .range([labelAreaWidth + 2, width - (total_nums_width + 2)]);

  $: histogramY = scaleLinear().domain([0, 15000]).range([0.8, 0.05]);

  $: barX = scaleLinear()
    .domain([0, 1])
    .range([labelAreaWidth + 2, width - (total_nums_width + 2)]);

  $: popY = scaleLinear().domain([0, 1]).range([0, height]);

  function labelX(pop) {
    if (!width) return 0;
    let total = 0;
    for (let i = 0; i < bboxArray.length; ++i) {
      if (pop.level >= i) {
        if (bboxArray[i]) {
          total += bboxArray[i].width;
        }
      }
    }
    return total;
  }

  $: minHeight =
    Math.pow(2, findLevels(aData)) * 30 * (hasHistograms ? 6 : 1) + "px";
</script>

<h3>
  {numbers.dx}
</h3>

<div
  class="sizer"
  bind:clientWidth={width}
  bind:clientHeight={height}
  width="80vw"
  style={`min-width:${labelAreaWidth + 2 * total_nums_width + 100}px`}
>
  {#if width && aData}
    <svg width="100%" height={minHeight}>
      <g>
        {#if height > 20}
          <text x={width} y="0" text-anchor="end" class="bolded">
            total n
          </text>
          {#each populationsWithGroupTotals(aData) as pop}
            {#if pop.total}
              <text text-anchor="end" x={width} y={popY(pop.yPlace(0.5)) + 5}>
                {pop.total.toLocaleString()}
              </text>
            {/if}
            {#each ["positive", "negative"] as value}
              <rect
                x={barX(pop.xScale(value == "positive" ? 0 : pop["positive"]))}
                width={0.5 + barX(pop.xScale(pop[value])) - barX(0)}
                y={popY(pop.yPlace(pop.slices.bars(0.1)))}
                height={popY(pop.yPlace(pop.slices.bars(0.9))) -
                  popY(pop.yPlace(pop.slices.bars(0.1)))}
                fill={colors[value]}
              />
            {/each}
            {#if pop.ci_low !== undefined && pop.ci_high !== undefined}
              <line
                x1={barX(pop.xScale(pop.ci_low * pop.total))}
                x2={barX(pop.xScale(pop.ci_high * pop.total))}
                y1={popY(pop.yPlace(pop.slices.bars(0.5)))}
                y2={popY(pop.yPlace(pop.slices.bars(0.5)))}
                stroke="black"
              />
              <text
                x={Math.min(
                  Math.min(
                    barX(pop.xScale(pop["positive"])) - 5,
                    barX(pop.xScale(pop.ci_low * pop.total)) - 2
                  ),
                  barX(0) + 10
                )}
                y={popY(pop.yPlace(pop.slices.bars(0.5))) + 5}
                text-anchor="start">{pop["positive"].toLocaleString()}</text
              >
            {/if}
            {#if pop.histogram}
              <path
                d={line()
                  .curve(curveBumpX)
                  .x((d) => histogramX(d.viralLoadLog))
                  .y((d) =>
                    popY(
                      pop.yPlace(pop.slices.histogram(pop.histogramY(d.count)))
                    )
                  )(pop.histogram)}
                style={`stroke: ${pop.color}; fill: ${colors["positive"]}`}
              />
            {/if}
          {/each}
        {/if}
      </g>
      {#each findPopulations(aData) as pop}
        {#if !pop.isLeaf}
          {#if true}
            <line
              x1={labelX(pop, bboxArray) + 4}
              x2={labelX(pop, bboxArray) + 4}
              y1={popY(pop.yPlace(0.03))}
              y2={popY(pop.yPlace(0.97))}
              stroke="grey"
            />
            <line
              x1={labelX(pop, bboxArray) + 4}
              x2={labelX(pop, bboxArray) + 14}
              y1={popY(pop.yPlace(0.03))}
              y2={popY(pop.yPlace(0.03))}
              stroke="grey"
            />
            <line
              x1={labelX(pop, bboxArray) + 4}
              x2={labelX(pop, bboxArray) + 14}
              y1={popY(pop.yPlace(0.97))}
              y2={popY(pop.yPlace(0.97))}
              stroke="grey"
            />
          {/if}
        {/if}
        {#if !pop.isLeaf}
          <text
            x={labelX(pop, bboxArray)}
            y={popY(pop.yPlace(0.5)) + 5}
            text-anchor="end"
          >
            {pop.label}
          </text>
        {/if}
      {/each}
      <g
        class="x-axis"
        transform={`translate(0, ${height + 2})`}
        overflow="visible"
      >
        <line x1={barX(0)} x2={barX(1)} y1="0" y2="0" stroke="black" />
        {#each [0.0, 0.2, 0.4, 0.6, 0.8, 1.0] as tick}
          <g class="tick" transform={`translate(${barX(tick)},0)`}>
            <foreignObject width="2.5em" height="2em" x="-0.5em" y="0.5em">
              <div class="exponentlabel">
                {Math.round(tick * 100)}%
              </div>
            </foreignObject>
            <line x1="0" x2="0" y1="0" y2="5" stroke="black" />
          </g>
        {/each}
      </g>
      {#if hasHistograms}
        <g class="x-axis" transform={`translate(0, -40)`}>
          <line
            x1={barX(0)}
            x2={histogramX(9)}
            y1="33"
            y2="33"
            stroke="black"
          />
          {#each [0, 3, 6, 9] as tick}
            <g class="tick" transform={`translate(${histogramX(tick)},0)`}>
              <foreignObject width="2em" height="2em" x="-0.5em" y="0.25em">
                <div class="exponentlabel">
                  10<sup>{tick}</sup>
                </div>
              </foreignObject>
              <line x1="0" x2="0" y1="33" y2="28" stroke="black" />
            </g>
          {/each}
        </g>
      {/if}

      <!-- Discreetly find out the text size of our labels -->
      {#each longestStrings as labelString, i}
        <text x="-1000" y="-1000" bind:this={stringSizeWidgetArray[i]}>
          M {labelString}
        </text>
      {/each}
      <text x="-1000" y="-1000" bind:this={strSizer_total}>
        {#if maxTotal}
          {maxTotal.toLocaleString()}
        {:else}
          0
        {/if}
      </text>
    </svg>
  {/if}
</div>

<style>
  div.sizer {
    margin-top: 20px;
    margin-right: 100px;
    margin-bottom: 20px;
    margin-left: 100px;
  }
  h3 {
    margin: auto;
    text-align: center;
  }
  svg {
    /* Note that both of these must be set to keep the graphic from going over the
      top menu banner: */
    position: relative;
    z-index: -1;
    overflow: visible;
  }
  .bolded {
    font-weight: bold;
  }
</style>
