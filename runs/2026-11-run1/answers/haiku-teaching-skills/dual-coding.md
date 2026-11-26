# Board diagram and script: how a coastal spit forms

I've assumed a Year 8 class, a whiteboard or a projector, and a 10-minute explanation. Use the SVG below as the finished diagram, or draw the same shapes by hand in the build order.

## The finished diagram

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="600" height="400" role="img" aria-labelledby="spit-title spit-desc">
  <title id="spit-title">How a spit forms</title>
  <desc id="spit-desc">Land at the top, sea below. A headland sticks out on the left. Waves approach at an angle, and longshore drift moves sand along the coast. A spit grows out from the headland across the bay, enclosing a lagoon behind it.</desc>
  <defs>
    <marker id="ah" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="#1f2937"/>
    </marker>
  </defs>
  <!-- 1. Sea -->
  <rect x="0" y="200" width="600" height="200" fill="#cfe8f5"/>
  <!-- 2. Land and coastline with headland and bay -->
  <path d="M0,0 L600,0 L600,160 Q480,170 400,160 L330,150 Q260,150 230,205 Q200,240 150,225 Q80,215 0,210 Z" fill="#efe6c8" stroke="#6b5b3e" stroke-width="2"/>
  <!-- 3. Waves approaching at an angle -->
  <line x1="40" y1="340" x2="120" y2="282" stroke="#1f2937" stroke-width="3" marker-end="url(#ah)"/>
  <!-- 4. Longshore drift -->
  <line x1="30" y1="262" x2="210" y2="262" stroke="#b45309" stroke-width="3" marker-end="url(#ah)"/>
  <!-- 5. Spit growing across the bay -->
  <path d="M230,205 Q280,222 330,220 Q380,218 410,234" fill="none" stroke="#d9b86c" stroke-width="12" stroke-linecap="round"/>
  <!-- 6. Lagoon behind the spit -->
  <ellipse cx="330" cy="188" rx="62" ry="12" fill="#8fc9e6"/>
  <!-- 7. Labels -->
  <text x="40" y="90" font-family="Arial, sans-serif" font-size="16" fill="#1f2937">Land</text>
  <text x="95" y="190" font-family="Arial, sans-serif" font-size="14" fill="#1f2937">Headland</text>
  <text x="430" y="330" font-family="Arial, sans-serif" font-size="16" fill="#1f2937">Sea</text>
  <text x="150" y="325" font-family="Arial, sans-serif" font-size="14" fill="#1f2937">Waves approach at an angle</text>
  <text x="30" y="252" font-family="Arial, sans-serif" font-size="14" fill="#1f2937">Longshore drift moves sand along the coast</text>
  <text x="270" y="186" font-family="Arial, sans-serif" font-size="13" fill="#1f2937">Lagoon</text>
  <text x="395" y="258" font-family="Arial, sans-serif" font-size="14" fill="#1f2937">Spit</text>
</svg>
```

## Build order and what to say

**Step 1. Draw the sea (bottom half).**
Say: "The sea is the bottom half of our picture. Everything at the top is land."

**Step 2. Draw the coastline.**
Draw a wavy line across the middle. Put a point of land sticking out on the left and a curve inwards on the right. Label the point "Headland".
Say: "This is the coastline. The headland is a piece of harder rock that sticks out into the sea."

**Step 3. Draw the waves.**
Draw one arrow hitting the coast at an angle, not straight on.
Say: "Waves usually come in at an angle, pushed by the wind. They hit the beach and wash sand up the beach at that same angle."

**Step 4. Draw longshore drift.**
Draw a long arrow running along the coast, from left to right.
Say: "The sand is carried along the coast in this direction. This movement is called longshore drift. Every wave moves a little sand sideways."

**Step 5. Draw the spit.**
Starting at the headland, draw a thick line that curves out across the bay. Label it "Spit".
Say: "Where the coast turns inwards, the drifting sand loses energy and drops. Over time it builds up into a long ridge that grows out from the headland. This ridge is the spit."

**Step 6. Add the lagoon.**
Shade the calm water between the spit and the bay coast. Label it "Lagoon".
Say: "The spit cuts off the bay from the open sea. The water behind it is calm, so it is called a lagoon."

**Step 7. Finish with a sentence.**
Say: "So a spit forms when longshore drift carries sand along the coast, and the sand is deposited where the coast changes direction."

## Blank version for students

Print or draw the diagram with the spit, the lagoon and all three arrows removed, and with the labels replaced by numbered boxes. Students fill in:

1. The sea and the land
2. The headland
3. The direction of waves and longshore drift
4. Where the spit forms and why
5. The lagoon

Ask them to write one sentence under the finished picture, starting "A spit forms because..."
