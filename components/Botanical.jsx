// Botanical placeholder — vintage engraving-style hatched rectangle
// with a small label underneath. Used wherever a real plant photo
// will eventually go. NEVER attempt to draw the actual plant.

function PlantPlaceholder({ label = 'plant photo', sublabel, ratio = '4 / 5', tone = 'sepia', frame = true, num }) {
  const tones = {
    sepia: { bg: '#e8dcbe', stripe1: 'rgba(60,45,20,0.22)', stripe2: 'rgba(60,45,20,0.10)' },
    moss:  { bg: '#cfd2b3', stripe1: 'rgba(40,55,25,0.28)', stripe2: 'rgba(40,55,25,0.12)' },
    rust:  { bg: '#dcc4a6', stripe1: 'rgba(110,55,20,0.25)', stripe2: 'rgba(110,55,20,0.10)' },
    grey:  { bg: '#d8cfb8', stripe1: 'rgba(40,30,20,0.22)', stripe2: 'rgba(40,30,20,0.10)' },
  };
  const t = tones[tone] || tones.sepia;
  const bg = {
    backgroundColor: t.bg,
    backgroundImage: [
      `repeating-linear-gradient(135deg, ${t.stripe1} 0 1px, transparent 1px 6px)`,
      `repeating-linear-gradient(45deg, ${t.stripe2} 0 1px, transparent 1px 9px)`,
      `radial-gradient(ellipse at 30% 30%, rgba(255,250,235,0.35), transparent 60%)`,
    ].join(', '),
  };
  return (
    <div style={{ width: '100%' }}>
      <div style={{
        position: 'relative',
        aspectRatio: ratio,
        ...bg,
        border: frame ? '1px solid rgba(60,45,20,0.55)' : 'none',
        outline: frame ? '4px solid var(--paper)' : 'none',
        outlineOffset: '-7px',
        boxShadow: frame ? 'inset 0 0 0 1px rgba(60,45,20,0.35)' : 'none',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'hidden',
      }}>
        {num && (
          <div style={{
            position: 'absolute', top: 10, left: 12,
            fontFamily: 'var(--display)', fontStyle: 'italic',
            fontSize: 14, color: 'var(--ink-soft)',
            background: 'var(--paper-light)', padding: '0 6px',
            border: '1px solid var(--rule)',
          }}>{num}</div>
        )}
        <div style={{
          fontFamily: 'var(--mono)', fontSize: 10,
          color: 'rgba(40,30,15,0.65)', textAlign: 'center',
          background: 'rgba(247,240,221,0.78)',
          padding: '6px 10px',
          border: '1px dashed rgba(60,45,20,0.45)',
          letterSpacing: '0.08em',
          textTransform: 'uppercase',
          maxWidth: '78%',
        }}>
          {label}
          {sublabel && <div style={{ marginTop: 2, opacity: 0.7, textTransform: 'none', letterSpacing: 0 }}>{sublabel}</div>}
        </div>
      </div>
    </div>
  );
}

// Pure-CSS fleuron divider
function Fleuron({ glyphs = '❦ ※ ❦', color }) {
  return (
    <div style={{
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      gap: 14, color: color || 'var(--rule)',
      fontFamily: 'var(--display)', fontSize: 16, letterSpacing: '0.3em',
      margin: '8px 0',
    }}>
      <span style={{ flex: 1, height: 1, background: 'currentColor', opacity: 0.5 }} />
      <span>{glyphs}</span>
      <span style={{ flex: 1, height: 1, background: 'currentColor', opacity: 0.5 }} />
    </div>
  );
}

// Plate number tag — like in a botanical reference
function PlateTag({ children }) {
  return (
    <span style={{
      fontFamily: 'var(--display-sc)',
      fontSize: 11, letterSpacing: '0.2em',
      color: 'var(--ink-soft)',
      border: '1px solid var(--rule)',
      padding: '2px 8px',
      background: 'var(--paper-light)',
    }}>{children}</span>
  );
}

Object.assign(window, { PlantPlaceholder, Fleuron, PlateTag });
