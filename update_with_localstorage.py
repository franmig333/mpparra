import re

with open('/Users/franmig33/Desktop/mpparra/index.html', 'r') as f:
    content = f.read()

# 1. ADD ADMIN STYLES
admin_styles = """
    /* ==========================================================================
       ADMIN STYLES (T-LEVA 2026)
       ========================================================================== */
    <style id="admin-styles">
        .t-leva-footer {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 15px;
            margin-top: 20px;
            opacity: 0.3;
            transition: opacity 0.3s;
            font-size: 10px;
            letter-spacing: 1px;
            color: var(--text-gray);
            z-index: 10;
            position: relative;
        }
        .t-leva-footer:hover { opacity: 0.8; }
        .t-leva-lock {
            margin-left: 8px;
            cursor: pointer;
            color: var(--gold-primary);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        #admin-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(10,11,13,0.9); backdrop-filter: blur(8px);
            z-index: 9999999; display: flex; justify-content: center; align-items: center;
            opacity: 0; pointer-events: none; transition: opacity 0.3s;
        }
        #admin-overlay.active { opacity: 1; pointer-events: auto; }
        
        #admin-panel {
            width: 90%; max-width: 600px; height: 85vh; max-height: 800px;
            background: #111317; border: 1px solid var(--gold-primary); border-radius: 16px;
            display: flex; flex-direction: column; overflow: hidden;
            transform: translateY(20px); transition: transform 0.3s;
            box-shadow: 0 20px 50px rgba(0,0,0,0.8);
            font-family: 'Montserrat', sans-serif;
        }
        #admin-overlay.active #admin-panel { transform: translateY(0); }
        
        .admin-header {
            padding: 20px; background: #0a0b0d; border-bottom: 1px solid rgba(223,186,107,0.2);
            display: flex; justify-content: space-between; align-items: center;
        }
        .admin-header h2 { font-size: 16px; color: var(--gold-primary); font-family: 'Cinzel', serif; margin:0;}
        
        .admin-tabs { display: flex; background: #16181c; border-bottom: 1px solid rgba(223,186,107,0.1); }
        .admin-tab { 
            padding: 12px 15px; font-size: 11px; color: #a4b0be; cursor: pointer; text-transform: uppercase; flex: 1; text-align: center;
            border-bottom: 2px solid transparent; transition: all 0.2s;
        }
        .admin-tab.active { color: var(--gold-primary); border-bottom-color: var(--gold-primary); font-weight: 600;}
        
        .admin-body { flex: 1; overflow-y: auto; padding: 20px; }
        .admin-body::-webkit-scrollbar { width: 5px; }
        .admin-body::-webkit-scrollbar-thumb { background: var(--gold-dark); border-radius: 5px; }
        
        .admin-tab-content { display: none; }
        .admin-tab-content.active { display: block; animation: fadeIn 0.3s; }
        @keyframes fadeIn { from{opacity:0;} to{opacity:1;} }
        
        .admin-group { margin-bottom: 20px; background: rgba(255,255,255,0.02); padding: 15px; border-radius: 8px; border: 1px solid rgba(223,186,107,0.1); }
        .admin-group label { display: block; font-size: 10px; color: #a4b0be; margin-bottom: 8px; text-transform: uppercase; font-weight: 500; }
        .admin-input { 
            width: 100%; padding: 10px; background: #0a0b0d; border: 1px solid rgba(223,186,107,0.3); color: white; border-radius: 6px; font-size: 12px; margin-bottom: 10px; font-family: inherit;
        }
        .admin-input:focus { outline: none; border-color: var(--gold-primary); }
        .admin-checkbox { display: flex; align-items: center; gap: 8px; font-size: 11px; color: white; margin-bottom: 10px; cursor: pointer;}
        .admin-hint { font-size: 9px; color: var(--gold-dark); margin-top: -5px; margin-bottom: 10px; display: block;}
        
        .admin-btn { background: rgba(223,186,107,0.1); color: var(--gold-primary); border: 1px solid var(--gold-primary); padding: 8px 12px; border-radius: 6px; cursor: pointer; font-size: 10px; text-transform: uppercase; font-weight: 600; display: inline-flex; align-items: center; gap: 5px;}
        .admin-btn:hover { background: var(--gold-primary); color: #0a0b0d; }
        
        .admin-item-row { display: flex; align-items: center; justify-content: space-between; background: #0a0b0d; padding: 10px; border-radius: 6px; margin-bottom: 8px; border: 1px solid rgba(223,186,107,0.1);}
        .admin-item-row .controls { display: flex; gap: 5px; }
        
        .admin-footer { padding: 15px 20px; background: #0a0b0d; border-top: 1px solid rgba(223,186,107,0.2); display: flex; justify-content: flex-end; gap: 10px;}
        .admin-btn-primary { background: var(--gold-gradient); color: black; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; text-transform: uppercase; font-size: 11px;}
        .admin-btn-primary:hover { box-shadow: 0 0 15px rgba(223,186,107,0.4); transform: translateY(-2px); }
    </style>
"""

content = content.replace('</style>', '</style>\n' + admin_styles)

# 2. ADD IDS TO HTML ELEMENTS FOR DYNAMIC RENDERING
content = re.sub(r'<div class="firm-title-text">.*?</div>', '<div class="firm-title-text" id="render-title"></div>', content)
content = re.sub(r'<div class="firm-subtitle-text">.*?</div>', '<div class="firm-subtitle-text" id="render-subtitle"></div>', content)
content = re.sub(r'<!-- Fila de 3 Botones -->.*?</div>\s*</div>', '<div id="render-buttons"></div>', content, flags=re.DOTALL)
content = re.sub(r'<div class="gallery-modal-body">.*?</div>\s*</div>\s*</div>', '<div class="gallery-modal-body" id="render-cases"></div>\n      </div>\n    </div>', content, flags=re.DOTALL)


# 3. ADD FOOTER & LOCK
footer_html = """
    <!-- Pie de página y Candado de Acceso -->
    <div class="t-leva-footer">
      Diseño web app: T-LEVA 2026
      <div class="t-leva-lock" onclick="abrirAdmin()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
      </div>
    </div>
"""
content = content.replace('<!-- Banner Toast de Notificación -->', footer_html + '\n    <!-- Banner Toast de Notificación -->')

# 4. ADD JS STATE AND RENDERING
js_state = r"""
    // ==========================================================================
    // ESTADO Y CONFIGURACIÓN (LOCALSTORAGE)
    // ==========================================================================
    const DEFAULT_CONFIG = {
      header: {
        title: "MP PARRA & ASOCIADOS",
        showTitle: true,
        subtitle: "Estudio Jurídico & Estrategia Pública",
        showSubtitle: true,
        logo: "https://res.cloudinary.com/drpuhj6mc/image/upload/v1779039483/LOGO_rjejdk.jpg",
        portrait: "image_4493e7.jpg"
      },
      contact: {
        whatsapp: "593994511585",
        phone: "+593 99 451 1585",
        email: "contacto@mpparra.com",
        instagram: "https://instagram.com",
        maps: "https://maps.google.com"
      },
      buttons: [
        { id: 'whatsapp', type: 'whatsapp', label: 'Mensaje', visible: true, order: 1 },
        { id: 'phone', type: 'phone', label: 'Teléfono', visible: true, order: 2 },
        { id: 'email', type: 'email', label: 'E-Mail', visible: true, order: 3 },
        { id: 'instagram', type: 'social', label: 'Red Social', visible: true, order: 4 },
        { id: 'maps', type: 'location', label: 'Localización', visible: true, order: 5 }
      ],
      cases: [
        { id: 1, tag: 'Derecho Corporativo', title: 'Reestructuración Empresarial', desc: 'Asesoría jurídica integral en fusiones, adquisiciones y reestructuración de pasivos para grandes consorcios nacionales y multinacionales.', image: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&q=80&w=400&h=200' },
        { id: 2, tag: 'Estrategia Pública', title: 'Contratación & Políticas Públicas', desc: 'Consultoría estratégica y representación legal de alta complejidad ante entidades reguladoras y contratación estatal de infraestructura.', image: 'https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&q=80&w=400&h=200' },
        { id: 3, tag: 'Litigio Premium', title: 'Defensa Tributaria & Financiera', desc: 'Defensa ante controversias fiscales de alta cuantía, logrando resoluciones favorables ante la administración pública y tribunales.', image: 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&q=80&w=400&h=200' }
      ]
    };

    let siteConfig = JSON.parse(localStorage.getItem('mpparra_config')) || DEFAULT_CONFIG;
    let EMAIL_DATA = siteConfig.contact.email;
    let PHONE_DATA = siteConfig.contact.phone;

    function renderApp() {
      EMAIL_DATA = siteConfig.contact.email;
      PHONE_DATA = siteConfig.contact.phone;

      // Textos
      const titleEl = document.getElementById('render-title');
      if (titleEl) {
        titleEl.innerText = siteConfig.header.title;
        titleEl.style.display = siteConfig.header.showTitle ? 'block' : 'none';
      }

      const subtitleEl = document.getElementById('render-subtitle');
      if (subtitleEl) {
        subtitleEl.innerText = siteConfig.header.subtitle;
        subtitleEl.style.display = siteConfig.header.showSubtitle ? 'block' : 'none';
      }

      // Imágenes
      const logoEl = document.getElementById('logoElement');
      if (logoEl) logoEl.src = siteConfig.header.logo;
      const portraitEl = document.getElementById('portraitElement');
      if (portraitEl) portraitEl.src = siteConfig.header.portrait;

      // Botones
      const btnsContainer = document.getElementById('render-buttons');
      if (btnsContainer) {
        let sortedBtns = [...siteConfig.buttons].filter(b => b.visible).sort((a, b) => a.order - b.order);
        let html = '<div class="grid-row-triple">';
        let inDouble = false;

        sortedBtns.forEach((btn, index) => {
          if (index === 3 && !inDouble) {
            html += '</div><div class="grid-row-double">';
            inDouble = true;
          }

          let icon = '';
          let action = '';
          let tag = 'a';
          
          if (btn.type === 'whatsapp') {
            icon = '<svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z"/></svg>';
            action = `href="https://wa.me/${siteConfig.contact.whatsapp.replace(/\D/g,'')}" target="_blank" onclick="alertConexion('${btn.label}')"`;
          } else if (btn.type === 'phone') {
            icon = '<svg viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>';
            action = `href="tel:${siteConfig.contact.phone.replace(/\s/g,'')}" onclick="alertConexion('${btn.label}')"`;
          } else if (btn.type === 'email') {
            tag = 'button';
            icon = '<svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>';
            action = `onclick="copiarEmail(event)"`;
          } else if (btn.type === 'social') {
            icon = '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3.2"/><path d="M9 2h6c3.87 0 7 3.13 7 7v6c0 3.87-3.13 7-7 7H9c-3.87 0-7-3.13-7-7V9c0-3.87 3.13-7 7-7zm0 1.5c-3.03 0-5.5 2.47-5.5 5.5v6c0 3.03 2.47 5.5 5.5 5.5h6c3.03 0 5.5-2.47 5.5-5.5V9c0-3.03-2.47-5.5-5.5-5.5H9zM18.5 4.5a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>';
            action = `href="${siteConfig.contact.instagram}" target="_blank" onclick="alertConexion('${btn.label}')"`;
          } else if (btn.type === 'location') {
            icon = '<svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>';
            action = `href="${siteConfig.contact.maps}" target="_blank" onclick="alertConexion('${btn.label}')"`;
          }

          html += `
            <${tag} ${action} class="btn-card-action">
              <div class="icon-gold-ring">${icon}</div>
              <span class="label-enmarcada">${btn.label}</span>
            </${tag}>
          `;
        });
        html += '</div>';
        btnsContainer.innerHTML = html;
      }

      // Casos
      const casesContainer = document.getElementById('render-cases');
      if (casesContainer) {
        let html = '';
        siteConfig.cases.forEach(c => {
          html += `
            <div class="case-gallery-card">
              <div class="case-card-image-box">
                <span class="case-card-tag">${c.tag}</span>
                <img src="${c.image}" alt="${c.title}" class="case-card-img">
              </div>
              <div class="case-card-info">
                <h3 class="case-card-title">${c.title}</h3>
                <p class="case-card-desc">${c.desc}</p>
              </div>
            </div>
          `;
        });
        casesContainer.innerHTML = html;
      }
    }

    window.addEventListener('DOMContentLoaded', () => {
      renderApp();
    });
"""

# Find the location to replace const EMAIL_DATA and const PHONE_DATA
match = re.search(r'const EMAIL_DATA\s*=\s*".*?";\s*const PHONE_DATA\s*=\s*".*?";', content)
if match:
    content = content[:match.start()] + js_state + content[match.end():]


# 5. ADD ADMIN PANEL HTML AND LOGIC AT THE END
admin_panel = """
  <!-- ==========================================================================
       ADMIN PANEL (FRONTEND)
       ========================================================================== -->
  <div id="admin-overlay">
    <div id="admin-panel">
      <div class="admin-header">
        <h2>Workspace T-LEVA</h2>
        <button class="admin-btn" onclick="cerrarAdmin()" style="border-color:transparent; color:#a4b0be; background:transparent;">✕ Salir</button>
      </div>
      
      <div class="admin-tabs">
        <div class="admin-tab active" onclick="switchTab('tab-textos', this)">Textos</div>
        <div class="admin-tab" onclick="switchTab('tab-media', this)">Imágenes</div>
        <div class="admin-tab" onclick="switchTab('tab-botones', this)">Enlaces</div>
        <div class="admin-tab" onclick="switchTab('tab-casos', this)">Casos</div>
      </div>
      
      <div class="admin-body">
        
        <!-- Pestaña Textos -->
        <div id="tab-textos" class="admin-tab-content active">
          <div class="admin-group">
            <label>Título Principal</label>
            <input type="text" class="admin-input" id="adm-title">
            <label class="admin-checkbox"><input type="checkbox" id="adm-show-title"> Mostrar Título en la Web</label>
          </div>
          <div class="admin-group">
            <label>Subtítulo</label>
            <input type="text" class="admin-input" id="adm-subtitle">
            <label class="admin-checkbox"><input type="checkbox" id="adm-show-subtitle"> Mostrar Subtítulo en la Web</label>
          </div>
        </div>
        
        <!-- Pestaña Imágenes -->
        <div id="tab-media" class="admin-tab-content">
          <div class="admin-group">
            <span class="admin-hint">Recomendación: Sube tus imágenes a <b>Cloudinary</b> o ImgBB y pega aquí la URL directa para no saturar el servidor.</span>
            <label>URL del Logotipo</label>
            <input type="text" class="admin-input" id="adm-logo">
            <br>
            <label>URL de la Foto de Perfil</label>
            <input type="text" class="admin-input" id="adm-portrait">
          </div>
        </div>
        
        <!-- Pestaña Botones -->
        <div id="tab-botones" class="admin-tab-content">
          <div class="admin-group">
            <label>WhatsApp (Número con código de país, sin +)</label>
            <input type="text" class="admin-input" id="adm-whatsapp">
            <label>Teléfono Base</label>
            <input type="text" class="admin-input" id="adm-phone">
            <label>Correo Electrónico</label>
            <input type="text" class="admin-input" id="adm-email">
            <label>URL Instagram</label>
            <input type="text" class="admin-input" id="adm-instagram">
            <label>URL Google Maps</label>
            <input type="text" class="admin-input" id="adm-maps">
          </div>
          
          <div class="admin-group">
            <label style="border-bottom: 1px solid rgba(223,186,107,0.2); padding-bottom: 10px; margin-bottom: 15px;">Orden y Visibilidad de Botones</label>
            <div id="adm-btns-list"></div>
          </div>
        </div>
        
        <!-- Pestaña Casos de Éxito -->
        <div id="tab-casos" class="admin-tab-content">
          <div id="adm-cases-list"></div>
          <button class="admin-btn" style="width: 100%; justify-content: center; padding: 12px; margin-top: 10px;" onclick="addCase()">+ Añadir Nuevo Caso</button>
        </div>
        
      </div>
      
      <div class="admin-footer">
        <button class="admin-btn-primary" onclick="guardarAdmin()">Guardar y Salir</button>
      </div>
    </div>
  </div>

  <script>
    let tempConfig = null;

    function abrirAdmin() {
      const p = prompt("Clave de Administración:");
      if (p === "admin") {
        tempConfig = JSON.parse(JSON.stringify(siteConfig)); // Clone state
        populateAdmin();
        document.getElementById('admin-overlay').classList.add('active');
        document.body.style.overflow = 'hidden';
      } else if (p) {
        alert("Clave incorrecta.");
      }
    }

    function cerrarAdmin() {
      document.getElementById('admin-overlay').classList.remove('active');
      document.body.style.overflow = '';
    }

    function switchTab(id, el) {
      document.querySelectorAll('.admin-tab-content').forEach(c => c.classList.remove('active'));
      document.querySelectorAll('.admin-tab').forEach(t => t.classList.remove('active'));
      document.getElementById(id).classList.add('active');
      el.classList.add('active');
    }

    function populateAdmin() {
      // Textos
      document.getElementById('adm-title').value = tempConfig.header.title;
      document.getElementById('adm-show-title').checked = tempConfig.header.showTitle;
      document.getElementById('adm-subtitle').value = tempConfig.header.subtitle;
      document.getElementById('adm-show-subtitle').checked = tempConfig.header.showSubtitle;
      
      // Media
      document.getElementById('adm-logo').value = tempConfig.header.logo;
      document.getElementById('adm-portrait').value = tempConfig.header.portrait;
      
      // Contactos
      document.getElementById('adm-whatsapp').value = tempConfig.contact.whatsapp;
      document.getElementById('adm-phone').value = tempConfig.contact.phone;
      document.getElementById('adm-email').value = tempConfig.contact.email;
      document.getElementById('adm-instagram').value = tempConfig.contact.instagram;
      document.getElementById('adm-maps').value = tempConfig.contact.maps;
      
      renderAdminBtnsList();
      renderAdminCasesList();
    }

    function renderAdminBtnsList() {
      const container = document.getElementById('adm-btns-list');
      let sorted = [...tempConfig.buttons].sort((a,b) => a.order - b.order);
      let html = '';
      
      sorted.forEach((btn, i) => {
        html += `
          <div class="admin-item-row">
            <label class="admin-checkbox" style="margin:0;"><input type="checkbox" ${btn.visible ? 'checked' : ''} onchange="toggleBtnVis('${btn.id}', this.checked)"> ${btn.label}</label>
            <div class="controls">
              <button class="admin-btn" onclick="moveBtn('${btn.id}', -1)" ${i===0 ? 'disabled style="opacity:0.3"' : ''}>▲</button>
              <button class="admin-btn" onclick="moveBtn('${btn.id}', 1)" ${i===sorted.length-1 ? 'disabled style="opacity:0.3"' : ''}>▼</button>
            </div>
          </div>
        `;
      });
      container.innerHTML = html;
    }

    function toggleBtnVis(id, vis) {
      const b = tempConfig.buttons.find(x => x.id === id);
      if(b) b.visible = vis;
    }

    function moveBtn(id, dir) {
      const idx = tempConfig.buttons.findIndex(b => b.id === id);
      if (idx === -1) return;
      const targetIdx = idx + dir;
      if (targetIdx >= 0 && targetIdx < tempConfig.buttons.length) {
        let temp = tempConfig.buttons[idx].order;
        tempConfig.buttons[idx].order = tempConfig.buttons[targetIdx].order;
        tempConfig.buttons[targetIdx].order = temp;
        tempConfig.buttons.sort((a,b) => a.order - b.order);
        renderAdminBtnsList();
      }
    }

    function renderAdminCasesList() {
      const container = document.getElementById('adm-cases-list');
      let html = '';
      tempConfig.cases.forEach((c, idx) => {
        html += `
          <div class="admin-group" style="position:relative; margin-bottom:15px;">
            <div style="position:absolute; top: 15px; right: 15px;">
              <button class="admin-btn" style="color: #ff6b6b; border-color:rgba(255,107,107,0.3); background:rgba(255,107,107,0.1);" onclick="deleteCase(${c.id})">Borrar</button>
            </div>
            <label>Caso #${idx+1}</label>
            <input type="text" class="admin-input" value="${c.tag}" oninput="updateCase(${c.id}, 'tag', this.value)" placeholder="Etiqueta (ej. Derecho Penal)">
            <input type="text" class="admin-input" value="${c.title}" oninput="updateCase(${c.id}, 'title', this.value)" placeholder="Título del caso">
            <input type="text" class="admin-input" value="${c.image}" oninput="updateCase(${c.id}, 'image', this.value)" placeholder="URL de la imagen">
            <textarea class="admin-input" style="min-height: 60px; resize:vertical;" oninput="updateCase(${c.id}, 'desc', this.value)" placeholder="Descripción...">${c.desc}</textarea>
          </div>
        `;
      });
      container.innerHTML = html;
    }

    function updateCase(id, field, value) {
      const c = tempConfig.cases.find(x => x.id === id);
      if (c) c[field] = value;
    }

    function deleteCase(id) {
      if(confirm("¿Seguro que deseas borrar este caso de éxito?")) {
        tempConfig.cases = tempConfig.cases.filter(x => x.id !== id);
        renderAdminCasesList();
      }
    }

    function addCase() {
      const newId = tempConfig.cases.length > 0 ? Math.max(...tempConfig.cases.map(x=>x.id)) + 1 : 1;
      tempConfig.cases.push({
        id: newId, tag: 'Nueva Área', title: 'Nuevo Caso', desc: 'Descripción del caso...', image: 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&q=80&w=400&h=200'
      });
      renderAdminCasesList();
    }

    function guardarAdmin() {
      // Leer valores de los inputs a tempConfig
      tempConfig.header.title = document.getElementById('adm-title').value;
      tempConfig.header.showTitle = document.getElementById('adm-show-title').checked;
      tempConfig.header.subtitle = document.getElementById('adm-subtitle').value;
      tempConfig.header.showSubtitle = document.getElementById('adm-show-subtitle').checked;
      
      tempConfig.header.logo = document.getElementById('adm-logo').value;
      tempConfig.header.portrait = document.getElementById('adm-portrait').value;
      
      tempConfig.contact.whatsapp = document.getElementById('adm-whatsapp').value;
      tempConfig.contact.phone = document.getElementById('adm-phone').value;
      tempConfig.contact.email = document.getElementById('adm-email').value;
      tempConfig.contact.instagram = document.getElementById('adm-instagram').value;
      tempConfig.contact.maps = document.getElementById('adm-maps').value;
      
      // Guardar en siteConfig y localStorage
      siteConfig = JSON.parse(JSON.stringify(tempConfig));
      localStorage.setItem('mpparra_config', JSON.stringify(siteConfig));
      
      // Renderizar y cerrar
      renderApp();
      cerrarAdmin();
      showNotificationToast("Cambios guardados exitosamente");
    }
  </script>
"""

content = content.replace('</body>', admin_panel + '\n</body>')

with open('/Users/franmig33/Desktop/mpparra/index.html', 'w') as f:
    f.write(content)
