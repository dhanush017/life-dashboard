# UI Polish Checklist — Senior Engineer Guidelines

This document outlines the refinement principles applied to Life Dashboard. Use this when making future UI updates.

---

## Core Principles

### 1. **Three-State Feedback for All Interactive Elements**
Every button, input, or clickable element should have three distinct states:
- **Default** — Normal appearance
- **Hover** — Visual feedback (transform: translateY, background shift, or shadow increase)
- **Active/Focus** — Pressed appearance (typically inverted transform or reduced shadow)

```css
.button {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}
.button:active {
    transform: translateY(0);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
```

---

### 2. **Consistent Transition Timing**
- **0.15s** — Too fast, feels janky
- **0.2-0.25s** ✅ — Sweet spot, feels responsive
- **0.3s+** — Feels sluggish

All transitions should use the same timing across the app.

---

### 3. **Layered Shadows = Depth**
Don't use single shadows. Layer them for realism:

```css
/* WRONG */
box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);

/* RIGHT */
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15), 0 8px 32px rgba(0, 0, 0, 0.2);
```

Multiple shadows at different distances = professional appearance.

---

### 4. **Intentional Spacing Scale**
Don't use arbitrary values. Follow a consistent scale:

```css
/* SPACING SCALE */
4px  — Micro spacing (gaps between icons)
8px  — Small (button padding variations)
12px — Standard padding
16px — Increased spacing
20px — Large sections
24px — Descriptions, margins
28px — Card padding
32px — Major sections
36px — Header padding
40px — Large sections
```

Avoid: 7px, 13px, 23px, 31px (feels random)

---

### 5. **Typography Hierarchy with Letter-Spacing**
- **Headings** — Use negative letter-spacing (-0.5px to -1px) for tightness
- **Body text** — Use small positive letter-spacing (0.2px to 0.3px) for readability
- **Labels** — Use bolder letter-spacing (0.7px to 1px) for clarity

```css
h1 {
    letter-spacing: -1px;  /* Tight, premium feel */
}
p {
    letter-spacing: 0.2px; /* Readable, intentional */
}
label {
    letter-spacing: 0.8px; /* Stands out, clear */
}
```

---

### 6. **Border Thickness Communicates Intent**
- **1px** — Subtle, almost disappears
- **1.5px** — Intentional, visible, premium ✅
- **2px** — Strong, primary accent

Use 1.5px as default for interactive elements.

---

### 7. **Hover State Should Communicate "Something Happens"**
Every hover state must be obvious. Pick ONE primary effect per element type:

- **Cards** — Transform + Shadow increase
- **Buttons** — Transform + Shadow increase + Optional background shift
- **Input fields** — Border color + Background shift + Shadow/glow
- **Table rows** — Subtle transform + Inset glow or background shift

---

### 8. **Opacity Consistency**
- **High emphasis** — 100% (var(--text-primary))
- **Medium emphasis** — 75-85% (var(--text-secondary))
- **Low emphasis** — 50-65% (var(--text-muted))
- **Very subtle** — 30-40% (hints, disabled states)

Never mix arbitrary opacities like 0.7 and 0.42. Stick to the hierarchy.

---

### 9. **Focus States for Accessibility**
Every focusable element needs a clear focus state (not just hover):

```css
input:focus,
button:focus {
    outline: 2px solid var(--accent-violet);
    outline-offset: 2px;
}
```

Or use box-shadow for glassmorphism:
```css
input:focus {
    box-shadow: 0 0 0 3px var(--accent-violet-dim);
}
```

---

### 10. **Avoid "Template Feel"**
❌ **Template-like:**
- All elements perfectly uniform
- Every hover state identical
- Mechanical animations
- Too many animations everywhere
- Generic color values

✅ **Handcrafted:**
- Slight variation in shadows/depths
- Each element has a unique hover feeling (but consistent language)
- Animations are purposeful, not decorative
- Strategic animation (80% of site is still, 20% is animated)
- Intentional color choices with clear semantics

---

## Quick Audit: Is Your UI Polish?

### Typography
- [ ] Headings are smaller than you'd expect (tighter line-height)
- [ ] Letter-spacing is intentional (not auto-fitted)
- [ ] Body text has consistent 1.5x line-height
- [ ] Labels are bolder than body text

### Interactions
- [ ] Every button has 3 states (default, hover, active)
- [ ] Hover state uses consistent transformation (usually -2 to -3px lift)
- [ ] Focus states are visible (high contrast, not just color change)
- [ ] All transitions use 0.2s or 0.25s timing

### Spacing
- [ ] Padding values follow 4/8/12/16/20/24/28/32 scale
- [ ] No random values like 7px, 13px, 23px
- [ ] Card padding is 28-32px, not 20px or 40px
- [ ] Margins between sections are consistent

### Shadows
- [ ] Cards have subtle drop shadow (0 2px 8px or similar)
- [ ] Buttons have visible shadow (0 4px 16px or similar)
- [ ] Hover states have increased shadows (layered)
- [ ] No single-shadow design (always 2+ layers)

### Colors
- [ ] Text hierarchy is clear (3 levels max: primary, secondary, muted)
- [ ] Border colors are intentional (not just "border-gray")
- [ ] Hover states change background slightly (rgba shift)
- [ ] Focus/active states are distinct from hover

---

## Common Mistakes to Avoid

❌ **Mistake 1:** Using `transition: all 0.3s ease`
- ✅ Fix: `transition: transform 0.2s ease, box-shadow 0.2s ease;`
- **Why:** Specific transitions, consistent timing

❌ **Mistake 2:** Different button styles everywhere
- ✅ Fix: 3 button types max (primary, secondary, tertiary)
- **Why:** Consistency = professionalism

❌ **Mistake 3:** Hover = color change only
- ✅ Fix: Hover = transform + shadow + color
- **Why:** Multiple feedbacks = user confidence

❌ **Mistake 4:** Opacity values like 0.47, 0.82, 0.33
- ✅ Fix: Use a hierarchy (1, 0.8, 0.6, 0.4)
- **Why:** Consistency = intentionality

❌ **Mistake 5:** Focus state is same as hover state
- ✅ Fix: Keyboard focus has outline or different shadow
- **Why:** Accessibility + distinct feedback

---

## Testing Your Refinements

### Visual Test
1. **Zoom to 200%** — Details should still look intentional, not break
2. **Zoom to 80%** — Overall composition should feel balanced
3. **Print to PDF** — Shadows/colors should translate

### Interaction Test
1. **Keyboard navigation** — Tab through all elements, focus states clear?
2. **Mobile hover** — Do hover states look weird on touch? (They might)
3. **Dark room** — Do contrast levels work in low light?
4. **Fast scroll** — Do animations feel smooth or janky?

### Comparison Test
1. **Before/After** — Is the new version obviously better?
2. **Competitor review** — How does it compare to Notion, Linear, Stripe?
3. **Screenshot at 1x/2x** — Does it scale well?

---

## Resources

### Shadow Generators
- https://www.shadowgenerator.com
- https://shadows.brumm.af

### Color Opacity
- Stick to: 1, 0.8, 0.6, 0.4, 0.2, 0.08

### Typography
- Line-height: 1.3-1.6 depending on size
- Letter-spacing: -0.5px to 0.5px for normal text

### Spacing
- Always use multiples of 4px (4, 8, 12, 16, 20, 24, 28, 32, 36, 40...)

---

## Summary

**Polish is about consistency and intentionality.**

Every decision should have a reason:
- Why is this button 14px padding and not 12px?
- Why does this shadow have two layers?
- Why does this text have 0.3px letter-spacing?

If you can't explain it, it's probably random. And random = template.

Senior engineers make it look effortless because every detail is deliberate.
