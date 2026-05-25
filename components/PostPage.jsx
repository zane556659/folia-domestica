// PostPage — 羽葉沒藥 / Commiphora monstruosa, real content from user

function PostPage() {
  const photos = [
    'https://i.ibb.co/TDsHvTV5/86006996862e.jpg',
    'https://i.ibb.co/bgx9sqrX/212a51ffc802.jpg',
    'https://i.ibb.co/RGkKgYRk/8ddcf34878dc.jpg',
  ];

  return (
    <div className="paper-texture" style={{
      minHeight: '100vh',
      fontFamily: 'var(--serif-body)',
      color: 'var(--ink)',
    }}>
      {/* Header — minimal masthead */}
      <header style={{
        maxWidth: 1180, margin: '0 auto', padding: '24px 40px 0',
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        borderBottom: '1px solid var(--rule)', paddingBottom: 16,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div style={{
            width: 32, height: 32, border: '1.5px solid var(--moss-deep)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontFamily: 'var(--display)', fontStyle: 'italic',
            fontSize: 18, color: 'var(--moss-deep)',
          }}>F</div>
          <div style={{ fontFamily: 'var(--display)', fontSize: 22, color: 'var(--moss-deep)' }}>
            家中花草志
          </div>
        </div>
        <a href="home.html" className="smcp" style={{ fontSize: 11, color: 'var(--ink-faded)', textDecoration: 'none' }}>
          ← 回首頁 · home
        </a>
      </header>

      {/* Article */}
      <article style={{ maxWidth: 760, margin: '0 auto', padding: '48px 40px 40px' }}>
        {/* Catalog header */}
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 12, marginBottom: 6 }}>
          <span style={{ fontFamily: 'var(--mono)', fontSize: 11, color: 'var(--ink-faded)' }}>№ 001</span>
          <span style={{ flex: 1, borderBottom: '1px dotted var(--rule)', marginBottom: 5 }} />
          <span style={{ fontFamily: 'var(--display)', fontStyle: 'italic', fontSize: 13, color: 'var(--ink-faded)' }}>
            2026 / 04 / 26
          </span>
        </div>

        <div className="smcp" style={{ fontSize: 11, color: 'var(--ink-faded)', marginBottom: 4 }}>
          多肉植物 — 塊根 — Commiphora (沒藥屬)
        </div>

        <h1 style={{
          margin: '8px 0 4px',
          fontFamily: 'var(--display)', fontWeight: 400,
          fontSize: 56, lineHeight: 1.05,
          color: 'var(--moss-deep)',
        }}>
          羽葉沒藥
        </h1>
        <div style={{ fontFamily: 'var(--display)', fontStyle: 'italic', fontSize: 22, color: 'var(--ink-soft)', marginBottom: 24 }}>
          Commiphora monstruosa
        </div>

        {/* Specimen meta block */}
        <div style={{
          border: '1px solid var(--rule)',
          background: 'var(--paper-light)',
          padding: '14px 18px', marginBottom: 22,
          display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px 28px',
        }}>
          <Meta en="Specimen" zh="標本" v="羽葉沒藥 · Commiphora monstruosa" />
          <Meta en="Photographed" zh="拍攝日期" v="2026 / 04 / 26" />
          <Meta en="Vigour" zh="生長狀況" v={<><span style={{ color: 'var(--moss)' }}>● 良好</span></>} />
          <Meta en="Catalog" zh="編號" v="№ HK-001" />
        </div>

        <Fleuron glyphs="❦" />

        {/* Hero photo */}
        <div style={{ margin: '24px 0' }}>
          <PhotoFrame src={photos[0]} caption="圖 一 · 換盆當日整體外觀（fig. i — overall, on repotting day）" />
        </div>

        {/* Lead — abstract */}
        <p style={{
          fontSize: 17, lineHeight: 1.75, textAlign: 'justify',
          color: 'var(--ink)',
          background: 'var(--paper-light)',
          borderLeft: '3px double var(--rule)',
          padding: '14px 18px', margin: '20px 0 0',
        }}>
          <span className="smcp" style={{ fontSize: 10, color: 'var(--ink-faded)', display: 'block', marginBottom: 6 }}>
            ABSTRACT · 摘要
          </span>
          一年未換盆，順便換盆並檢查根系。根系尚可但無白根。原介質太貧瘠加上施肥不勤導致長勢差，希望換介質後好轉。
          本次採用「<i>高透氣與石生模擬</i>」配方，排除赤玉土，並加入鈣粉以強化木質化。
        </p>

        {/* TOC */}
        <ul style={{
          listStyle: 'none', padding: 0, margin: '20px 0 0',
          display: 'flex', gap: 16, fontSize: 13,
          fontFamily: 'var(--display-sc)', letterSpacing: '0.2em',
        }}>
          <li><a style={{ color: 'var(--rust)', cursor: 'pointer' }}>I. 種植日記 →</a></li>
          <li><a style={{ color: 'var(--rust)', cursor: 'pointer' }}>II. 介質配方 →</a></li>
          <li><a style={{ color: 'var(--rust)', cursor: 'pointer' }}>III. 設計邏輯 →</a></li>
        </ul>

        <Fleuron glyphs="※ ※ ※" />

        {/* Section I — Cultivation Log */}
        <SectionHeader num="I." en="Cultivation Log" zh="種植日記 · 2026 / 04 / 26" />
        <p style={paraStyle}>
          一年未換盆，順便換盆並檢查根系。根系尚可<strong style={{ color: 'var(--moss-deep)' }}>但無白根</strong>。
          原介質太貧瘠加上施肥不勤導致長勢差，希望換介質後好轉。
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 18, margin: '24px 0' }}>
          <PhotoFrame src={photos[1]} caption="圖 二 · 脫盆後根系觀察（fig. ii — root inspection）" small />
          <PhotoFrame src={photos[2]} caption="圖 三 · 換盆後（fig. iii — after repotting）" small />
        </div>

        {/* Section II — Substrate */}
        <SectionHeader num="II." en="Substrate Recipe" zh="介質配方" />
        <div style={{
          border: '1px solid var(--rule)', background: 'var(--paper-light)',
          padding: '18px 22px', margin: '14px 0',
        }}>
          <SubstrateRow label="單純細顆粒" en="fine mineral grain" pct={50} />
          <SubstrateRow label="桐生砂" en="Kiryu sand" pct={30} />
          <SubstrateRow label="活性碳" en="activated charcoal" pct={15} />
          <SubstrateRow label="鈣粉" en="calcium powder" pct={5} last />
          <div style={{
            marginTop: 14, paddingTop: 12, borderTop: '1px dotted var(--rule)',
            display: 'flex', justifyContent: 'space-between', alignItems: 'baseline',
            fontFamily: 'var(--display)', fontStyle: 'italic', fontSize: 14, color: 'var(--ink-soft)',
          }}>
            <span>合計 · summa</span>
            <span style={{ fontFamily: 'var(--mono)', fontStyle: 'normal', color: 'var(--ink)' }}>100 %</span>
          </div>
        </div>

        {/* Section III — Design Logic */}
        <SectionHeader num="III." en="Design Logic" zh="設計邏輯與防禦目標" />
        <p style={paraStyle}>
          <strong style={{ color: 'var(--moss-deep)' }}>高透氣與石生模擬</strong> ——
          排除赤玉土，完全依靠礦物間隙通氣；鈣粉強化細弱枝幹的木質化速度。
        </p>
        <p style={paraStyle}>
          <strong style={{ color: 'var(--rust)' }}>防禦目標</strong> ——
          防止休眠期因環境濕度過高導致的「<i>塊根心腐</i>」。
        </p>

        <Fleuron glyphs="❦ ❦ ❦" />

        {/* Share strip */}
        <div style={{
          marginTop: 32, padding: '14px 0',
          borderTop: '1px solid var(--rule)', borderBottom: '1px solid var(--rule)',
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          fontFamily: 'var(--display-sc)', fontSize: 11, letterSpacing: '0.2em', color: 'var(--ink-faded)',
        }}>
          <span>取得連結 · 分享</span>
          <div style={{ display: 'flex', gap: 16 }}>
            <span style={{ cursor: 'pointer' }}>facebook</span>
            <span style={{ cursor: 'pointer' }}>x</span>
            <span style={{ cursor: 'pointer' }}>pinterest</span>
            <span style={{ cursor: 'pointer' }}>email</span>
          </div>
        </div>

        {/* Comments */}
        <div style={{ marginTop: 36 }}>
          <div style={{ fontFamily: 'var(--display)', fontSize: 22, color: 'var(--moss-deep)' }}>
            張貼留言
          </div>
          <div style={{ borderTop: '1px solid var(--rule)', marginTop: 8, marginBottom: 16 }} />
          <div style={{ fontSize: 13, color: 'var(--ink-faded)', fontStyle: 'italic', marginBottom: 14 }}>
            還沒有留言。當第一個吧。
          </div>
          <div style={{
            padding: 14,
            background: 'var(--paper-light)', border: '1px solid var(--rule)',
          }}>
            <div className="smcp" style={{ fontSize: 10, color: 'var(--ink-faded)', marginBottom: 8 }}>
              留下你的看法 · leave a comment
            </div>
            <div style={{
              minHeight: 60, borderBottom: '1px dotted var(--rule)',
              fontFamily: 'var(--mono)', fontSize: 12, color: 'var(--ink-faded)',
              padding: '6px 0',
            }}>
              ✎ ＿＿＿＿＿＿＿＿＿＿
            </div>
            <button style={{
              marginTop: 10,
              fontFamily: 'var(--display-sc)', letterSpacing: '0.2em', fontSize: 11,
              padding: '6px 18px', background: 'var(--moss-deep)', color: 'var(--paper-light)',
              border: 'none', cursor: 'pointer',
            }}>POST · 發表</button>
          </div>
        </div>
      </article>

      <footer style={{ borderTop: '3px double var(--rule)', background: 'var(--paper-light)' }}>
        <div style={{
          maxWidth: 1180, margin: '0 auto', padding: '24px 40px',
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          fontFamily: 'var(--display-sc)', fontSize: 11, letterSpacing: '0.2em',
          color: 'var(--ink-faded)',
        }}>
          <span>—— Folia Domestica ——</span>
          <span style={{ fontStyle: 'italic', fontFamily: 'var(--display)', textTransform: 'none', letterSpacing: 0 }}>
            這是第一篇 &nbsp;|&nbsp; 下一篇 · 待補 →
          </span>
          <span>MMXXVI</span>
        </div>
      </footer>
    </div>
  );
}

const paraStyle = { fontSize: 16, lineHeight: 1.85, color: 'var(--ink)', textAlign: 'justify', margin: '14px 0' };

function SectionHeader({ num, en, zh }) {
  return (
    <div style={{ marginTop: 32, marginBottom: 8 }}>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 12 }}>
        <span style={{ fontFamily: 'var(--display)', fontStyle: 'italic', fontSize: 28, color: 'var(--rust)' }}>{num}</span>
        <span style={{ fontFamily: 'var(--display)', fontSize: 28, color: 'var(--moss-deep)' }}>{en}</span>
        <span style={{ flex: 1, borderBottom: '1px solid var(--rule)', marginBottom: 8 }} />
        <span className="smcp" style={{ fontSize: 11, color: 'var(--ink-faded)' }}>{zh}</span>
      </div>
    </div>
  );
}

function Meta({ en, zh, v }) {
  return (
    <div style={{ display: 'flex', alignItems: 'baseline', gap: 10 }}>
      <div style={{ minWidth: 90 }}>
        <div className="smcp" style={{ fontSize: 9, color: 'var(--ink-faded)' }}>{en}</div>
        <div style={{ fontFamily: 'var(--display)', fontStyle: 'italic', fontSize: 12, color: 'var(--ink-soft)' }}>{zh}</div>
      </div>
      <div style={{ flex: 1, fontSize: 14, color: 'var(--ink)', fontFamily: 'var(--serif-body)' }}>
        {v}
      </div>
    </div>
  );
}

function PhotoFrame({ src, caption, small }) {
  return (
    <figure style={{ margin: 0 }}>
      <div style={{
        position: 'relative',
        aspectRatio: small ? '4 / 3' : '3 / 2',
        backgroundImage: `url(${src})`,
        backgroundSize: 'cover', backgroundPosition: 'center',
        border: '1px solid rgba(60,45,20,0.55)',
        outline: '4px solid var(--paper)',
        outlineOffset: '-7px',
        filter: 'sepia(0.18) contrast(0.96) saturate(0.9)',
      }} />
      <figcaption style={{
        textAlign: 'center', marginTop: 8,
        fontFamily: 'var(--display)', fontStyle: 'italic',
        fontSize: small ? 11 : 13, color: 'var(--ink-faded)',
      }}>{caption}</figcaption>
    </figure>
  );
}

function SubstrateRow({ label, en, pct, last }) {
  return (
    <div style={{
      display: 'flex', alignItems: 'center', gap: 14,
      padding: '8px 0',
      borderBottom: last ? 'none' : '1px dotted rgba(138,122,92,0.4)',
    }}>
      <div style={{ minWidth: 130 }}>
        <div style={{ fontSize: 15, color: 'var(--ink)' }}>{label}</div>
        <div style={{ fontFamily: 'var(--display)', fontStyle: 'italic', fontSize: 11, color: 'var(--ink-faded)' }}>{en}</div>
      </div>
      <div style={{
        flex: 1, height: 14,
        border: '1px solid var(--rule)', background: 'var(--paper)',
        position: 'relative', overflow: 'hidden',
      }}>
        <div style={{
          width: `${pct}%`, height: '100%',
          background: 'repeating-linear-gradient(45deg, var(--moss-deep) 0 4px, var(--moss) 4px 8px)',
        }} />
      </div>
      <div style={{
        minWidth: 50, textAlign: 'right',
        fontFamily: 'var(--mono)', fontSize: 13, color: 'var(--ink)',
      }}>{pct} %</div>
    </div>
  );
}

window.PostPage = PostPage;
