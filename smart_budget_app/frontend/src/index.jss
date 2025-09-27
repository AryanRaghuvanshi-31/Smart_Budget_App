/*
  This file imports the base Tailwind CSS styles.
  It should be the primary CSS file imported by main.jsx.
*/

@tailwind base;
@tailwind components;
@tailwind utilities;

/* Optional: Smooth transition for active tab */
.transition-colors {
  transition-property: background-color, border-color, color, fill, stroke, opacity, box-shadow, transform;
  transition-duration: 150ms;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}