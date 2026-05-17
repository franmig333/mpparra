import re

with open('/Users/franmig33/Desktop/mpparra/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix the CSS comment issue
content = content.replace("</style>\n  /* ==========================================================================\n     ADMIN STYLES (T-LEVA 2026)", "/* ==========================================================================\n     ADMIN STYLES (T-LEVA 2026)")
content = content.replace('     ========================================================================== */\n  <style id="admin-styles">', '     ========================================================================== */\n')

if '<style id="admin-styles">' not in content:
    content = re.sub(
        r'</style>\s*/\*\s*={10,}\s*ADMIN STYLES \(T-LEVA 2026\)\s*={10,}\s*\*/\s*<style id="admin-styles">',
        '</style>\n  <style id="admin-styles">\n    /* ADMIN STYLES (T-LEVA 2026) */',
        content
    )
content = content.replace('/* ==========================================================================\n     ADMIN STYLES (T-LEVA 2026)\n     ========================================================================== */\n  <style id="admin-styles">', '<style id="admin-styles">\n  /* ADMIN STYLES (T-LEVA 2026) */')
content = re.sub(r'</style>\n\s*/\*.*ADMIN STYLES.*?\*/\n\s*<style id="admin-styles">', '</style>\n  <style id="admin-styles">\n    /* ADMIN STYLES (T-LEVA 2026) */', content, flags=re.DOTALL)


# 2. Update CLOUDINARY constants and logic
js_cloudinary = """
    // ==========================================================================
    // ESTADO Y CONFIGURACIÓN (LOCALSTORAGE)
    // ==========================================================================
    const CLOUDINARY_CLOUD_NAME = 'tu_cloud_name'; // Ej. 'drpuhj6mc'
    const CLOUDINARY_UPLOAD_PRESET = 'tu_upload_preset'; // Debe ser un preset Unsigned
"""
content = re.sub(r'// ==========================================================================\n\s*// ESTADO Y CONFIGURACIÓN \(LOCALSTORAGE\)\n\s*// ==========================================================================', lambda m: js_cloudinary, content)


# 3. Update DEFAULT_CONFIG
new_config = """
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
        maps: "https://maps.google.com"
      },
      buttons: [
        { id: 'whatsapp', type: 'whatsapp', label: 'Mensaje', visible: true, order: 1 },
        { id: 'phone', type: 'phone', label: 'Teléfono', visible: true, order: 2 },
        { id: 'email', type: 'email', label: 'E-Mail', visible: true, order: 3 },
        { id: 'maps', type: 'location', label: 'Localización', visible: true, order: 4 }
      ],
      socials: [
        { id: 'soc_1', platform: 'Instagram', url: 'https://instagram.com', visible: true, order: 1 }
      ],
      cases: [
        { id: 1, tag: 'Derecho Corporativo', title: 'Reestructuración Empresarial', desc: 'Asesoría jurídica integral en fusiones, adquisiciones y reestructuración de pasivos para grandes consorcios nacionales y multinacionales.', image: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&q=80&w=400&h=200', visible: true, order: 1 },
        { id: 2, tag: 'Estrategia Pública', title: 'Contratación & Políticas Públicas', desc: 'Consultoría estratégica y representación legal de alta complejidad ante entidades reguladoras y contratación estatal de infraestructura.', image: 'https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&q=80&w=400&h=200', visible: true, order: 2 },
        { id: 3, tag: 'Litigio Premium', title: 'Defensa Tributaria & Financiera', desc: 'Defensa ante controversias fiscales de alta cuantía, logrando resoluciones favorables ante la administración pública y tribunales.', image: 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&q=80&w=400&h=200', visible: true, order: 3 }
      ]
    };

    let siteConfig = JSON.parse(localStorage.getItem('mpparra_config')) || DEFAULT_CONFIG;
    
    // Migración de datos antiguos (si el localStorage anterior no tenía 'socials' ni visibilidad en 'cases')
    if(!siteConfig.socials) {
        siteConfig.socials = [];
        if(siteConfig.contact.instagram) {
            siteConfig.socials.push({ id: 'soc_' + Date.now(), platform: 'Instagram', url: siteConfig.contact.instagram, visible: true, order: 1 });
        }
        siteConfig.buttons = siteConfig.buttons.filter(b => b.id !== 'instagram');
    }
    if(siteConfig.cases.length > 0 && typeof siteConfig.cases[0].visible === 'undefined') {
        siteConfig.cases.forEach((c, idx) => { c.visible = true; c.order = idx + 1; });
    }
"""
content = re.sub(r'const DEFAULT_CONFIG = \{.*?let siteConfig = JSON\.parse\(localStorage\.getItem\(\'mpparra_config\'\)\) \|\| DEFAULT_CONFIG;', lambda m: new_config, content, flags=re.DOTALL)


# 4. Update the renderApp() to handle Socials
render_socials_logic = """
      // Socials Logic (Icon generation)
      function getSocialIcon(name) {
          const n = name.toLowerCase();
          if(n.includes('instagram')) return '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3.2"/><path d="M9 2h6c3.87 0 7 3.13 7 7v6c0 3.87-3.13 7-7 7H9c-3.87 0-7-3.13-7-7V9c0-3.87 3.13-7 7-7zm0 1.5c-3.03 0-5.5 2.47-5.5 5.5v6c0 3.03 2.47 5.5 5.5 5.5h6c3.03 0 5.5-2.47 5.5-5.5V9c0-3.03-2.47-5.5-5.5-5.5H9zM18.5 4.5a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>';
          if(n.includes('facebook')) return '<svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12c0 4.84 3.44 8.87 8 9.8V15H8v-3h2V9.5C10 7.57 11.57 6 13.5 6H16v3h-2c-.55 0-1 .45-1 1v2h3v3h-3v6.8c4.56-.93 8-4.96 8-9.8 0-5.52-4.48-10-10-10z"/></svg>';
          if(n.includes('linkedin')) return '<svg viewBox="0 0 24 24"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.32 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.79M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>';
          if(n.includes('tiktok')) return '<svg viewBox="0 0 24 24"><path d="M12.53.02C13.84 0 15.14.01 16.44 0c.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.12-3.44-3.17-3.64-5.46-.22-2.39.87-4.82 2.87-6.09 1.56-.99 3.52-1.25 5.31-.83V14c-1.38-.28-2.88.2-3.67 1.39-.77 1.16-.62 2.84.34 3.82.9.91 2.37 1.19 3.55.67 1.3-.57 2.06-1.92 2.05-3.32.02-5.43 0-10.86.02-16.29V.02z"/></svg>';
          if(n.includes('youtube')) return '<svg viewBox="0 0 24 24"><path d="M21.58 7.19c-.23-.86-.91-1.54-1.77-1.77C18.25 5 12 5 12 5s-6.25 0-7.81.42c-.86.23-1.54.91-1.77 1.77C2 8.75 2 12 2 12s0 3.25.42 4.81c.23.86.91 1.54 1.77 1.77C5.75 19 12 19 12 19s6.25 0 7.81-.42c.86-.23 1.54-.91 1.77-1.77C22 15.25 22 12 22 12s0-3.25-.42-4.81zM9.5 15.5v-7l6 3.5-6 3.5z"/></svg>';
          if(n.includes('x') || n.includes('twitter')) return '<svg viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>';
          // Generic link
          return '<svg viewBox="0 0 24 24"><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"/></svg>';
      }
"""

replacement_for_render_buttons = """
      // Botones
      const btnsContainer = document.getElementById('render-buttons');
      if (btnsContainer) {
        let sortedBtns = [...siteConfig.buttons].filter(b => b.visible).sort((a, b) => a.order - b.order);
        let sortedSocials = [...siteConfig.socials].filter(s => s.visible).sort((a, b) => a.order - b.order);
        
        let allLinks = [];
        sortedBtns.forEach(b => allLinks.push({ ...b, isSocial: false }));
        sortedSocials.forEach(s => allLinks.push({ ...s, isSocial: true }));

        let html = '<div class="grid-row-triple">';
        let inDouble = false;

        allLinks.forEach((item, index) => {
          if (index === 3 && !inDouble) {
            html += '</div><div class="grid-row-double">';
            inDouble = true;
          }

          let icon = '';
          let action = '';
          let tag = 'a';
          
          if(item.isSocial) {
              icon = getSocialIcon(item.platform);
              action = `href="${item.url}" target="_blank" onclick="alertConexion('${item.platform}')"`;
          } else {
              if (item.type === 'whatsapp') {
                icon = '<svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z"/></svg>';
                action = `href="https://wa.me/${siteConfig.contact.whatsapp.replace(/\D/g,'')}" target="_blank" onclick="alertConexion('${item.label}')"`;
              } else if (item.type === 'phone') {
                icon = '<svg viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>';
                action = `href="tel:${siteConfig.contact.phone.replace(/\s/g,'')}" onclick="alertConexion('${item.label}')"`;
              } else if (item.type === 'email') {
                tag = 'button';
                icon = '<svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>';
                action = `onclick="copiarEmail(event)"`;
              } else if (item.type === 'location') {
                icon = '<svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>';
                action = `href="${siteConfig.contact.maps}" target="_blank" onclick="alertConexion('${item.label}')"`;
              }
          }

          let titleText = item.isSocial ? item.platform : item.label;

          html += `
            <${tag} ${action} class="btn-card-action">
              <div class="icon-gold-ring">${icon}</div>
              <span class="label-enmarcada">${titleText}</span>
            </${tag}>
          `;
        });
        html += '</div>';
        btnsContainer.innerHTML = html;
      }
"""
content = re.sub(r'// Botones.*?btnsContainer\.innerHTML = html;\n\s*\}', lambda m: render_socials_logic + '\n' + replacement_for_render_buttons, content, flags=re.DOTALL)


# 5. Render Cases logic update
replacement_for_render_cases = """
      // Casos
      const casesContainer = document.getElementById('render-cases');
      if (casesContainer) {
        let sortedCases = [...siteConfig.cases].filter(c => c.visible !== false).sort((a,b) => (a.order||0) - (b.order||0));
        let html = '';
        sortedCases.forEach(c => {
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
"""
content = re.sub(r'// Casos.*?casesContainer\.innerHTML = html;\n\s*\}', lambda m: replacement_for_render_cases, content, flags=re.DOTALL)


# 6. Admin Panel UI & Logic Updates
admin_html_start = """
  <!-- ==========================================================================
       ADMIN PANEL (FRONTEND)
       ========================================================================== -->
  <div id="admin-overlay">
    <div id="admin-panel">
      <div class="admin-header">
        <h2>WORKSPACE T-LEVA</h2>
        <button class="admin-btn" onclick="cerrarAdmin()" style="border-color:transparent; color:#a4b0be; background:transparent;">✕ Salir</button>
      </div>
"""
content = re.sub(r'<!-- ==========================================================================\n\s*ADMIN PANEL \(FRONTEND\)\n\s*========================================================================== -->.*?<div class="admin-header">.*?</div>', lambda m: admin_html_start, content, flags=re.DOTALL)

# Tab content replacements
tab_media = """
        <!-- Pestaña Imágenes -->
        <div id="tab-media" class="admin-tab-content">
          <div class="admin-group">
            <span class="admin-hint">Sube tus imágenes directamente. Las imágenes se alojarán en Cloudinary automáticamente.</span>
            
            <label>Logotipo</label>
            <div style="display:flex; gap:10px; margin-bottom:10px;">
                <input type="text" class="admin-input" id="adm-logo" style="margin-bottom:0;" placeholder="URL del logo">
                <button class="admin-btn-primary" id="btn-upload-logo" onclick="document.getElementById('file-logo').click()">SUBIR IMAGEN</button>
                <input type="file" id="file-logo" hidden accept="image/*" onchange="uploadImage(this, 'adm-logo', 'btn-upload-logo')">
            </div>
            
            <br>
            <label>Foto de Perfil</label>
            <div style="display:flex; gap:10px; margin-bottom:10px;">
                <input type="text" class="admin-input" id="adm-portrait" style="margin-bottom:0;" placeholder="URL del retrato">
                <button class="admin-btn-primary" id="btn-upload-portrait" onclick="document.getElementById('file-portrait').click()">SUBIR IMAGEN</button>
                <input type="file" id="file-portrait" hidden accept="image/*" onchange="uploadImage(this, 'adm-portrait', 'btn-upload-portrait')">
            </div>
          </div>
        </div>
"""
content = re.sub(r'<!-- Pestaña Imágenes -->.*?</div>\s*</div>', lambda m: tab_media, content, flags=re.DOTALL)

tab_botones = """
        <!-- Pestaña Botones -->
        <div id="tab-botones" class="admin-tab-content">
          <div class="admin-group">
            <label>WhatsApp (Número con código de país, sin +)</label>
            <input type="text" class="admin-input" id="adm-whatsapp">
            <label>Teléfono Base</label>
            <input type="text" class="admin-input" id="adm-phone">
            <label>Correo Electrónico</label>
            <input type="text" class="admin-input" id="adm-email">
            <label>URL Google Maps</label>
            <input type="text" class="admin-input" id="adm-maps">
          </div>
          
          <div class="admin-group">
            <label style="border-bottom: 1px solid rgba(223,186,107,0.2); padding-bottom: 10px; margin-bottom: 15px;">Botones Principales</label>
            <div id="adm-btns-list"></div>
          </div>

          <div class="admin-group">
            <label style="border-bottom: 1px solid rgba(223,186,107,0.2); padding-bottom: 10px; margin-bottom: 15px;">Redes Sociales (Dinámico)</label>
            <div id="adm-socials-list"></div>
            <button class="admin-btn" style="width: 100%; justify-content: center; padding: 12px; margin-top: 10px;" onclick="addSocial()">+ AÑADIR NUEVA RED SOCIAL</button>
          </div>
        </div>
"""
content = re.sub(r'<!-- Pestaña Botones -->.*?</div>\s*</div>', lambda m: tab_botones, content, flags=re.DOTALL)


# Update JS logic inside admin panel
new_admin_js = """
  <script>
    let tempConfig = null;

    async function uploadImage(fileInput, targetInputId, btnId) {
        if(!CLOUDINARY_CLOUD_NAME || !CLOUDINARY_UPLOAD_PRESET || CLOUDINARY_CLOUD_NAME === 'tu_cloud_name') {
            alert('Por favor configura CLOUDINARY_CLOUD_NAME y CLOUDINARY_UPLOAD_PRESET en el código HTML.');
            return;
        }

        const file = fileInput.files[0];
        if(!file) return;

        const btn = document.getElementById(btnId);
        const originalText = btn.innerText;
        btn.innerText = "Cargando...";
        btn.disabled = true;
        btn.style.opacity = "0.5";

        const formData = new FormData();
        formData.append('file', file);
        formData.append('upload_preset', CLOUDINARY_UPLOAD_PRESET);

        try {
            const res = await fetch(`https://api.cloudinary.com/v1_1/${CLOUDINARY_CLOUD_NAME}/image/upload`, {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            
            if(data.secure_url) {
                const targetInput = document.getElementById(targetInputId);
                targetInput.value = data.secure_url;
                
                if(targetInput.oninput) targetInput.oninput({target: targetInput});
                
                showNotificationToast("Imagen subida correctamente");
            } else {
                alert("Error al subir la imagen: " + (data.error ? data.error.message : 'Desconocido'));
            }
        } catch(e) {
            console.error(e);
            alert("Hubo un problema de conexión con Cloudinary.");
        } finally {
            btn.innerText = originalText;
            btn.disabled = false;
            btn.style.opacity = "1";
            fileInput.value = "";
        }
    }

    function abrirAdmin() {
      const p = prompt("Clave de Administración:");
      if (p === "admin") {
        tempConfig = JSON.parse(JSON.stringify(siteConfig));
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
      document.getElementById('adm-title').value = tempConfig.header.title;
      document.getElementById('adm-show-title').checked = tempConfig.header.showTitle;
      document.getElementById('adm-subtitle').value = tempConfig.header.subtitle;
      document.getElementById('adm-show-subtitle').checked = tempConfig.header.showSubtitle;
      
      document.getElementById('adm-logo').value = tempConfig.header.logo;
      document.getElementById('adm-portrait').value = tempConfig.header.portrait;
      
      document.getElementById('adm-whatsapp').value = tempConfig.contact.whatsapp;
      document.getElementById('adm-phone').value = tempConfig.contact.phone;
      document.getElementById('adm-email').value = tempConfig.contact.email;
      document.getElementById('adm-maps').value = tempConfig.contact.maps;
      
      renderAdminBtnsList();
      renderAdminSocialsList();
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

    function renderAdminSocialsList() {
      const container = document.getElementById('adm-socials-list');
      let sorted = [...tempConfig.socials].sort((a,b) => a.order - b.order);
      let html = '';
      
      sorted.forEach((soc, i) => {
        html += `
          <div class="admin-group" style="position:relative; margin-bottom:10px;">
            <div style="position:absolute; top: 15px; right: 15px; display:flex; gap:5px;">
              <button class="admin-btn" onclick="moveSocial('${soc.id}', -1)" ${i===0 ? 'disabled style="opacity:0.3"' : ''}>▲</button>
              <button class="admin-btn" onclick="moveSocial('${soc.id}', 1)" ${i===sorted.length-1 ? 'disabled style="opacity:0.3"' : ''}>▼</button>
              <button class="admin-btn" style="color: #ff6b6b; border-color:rgba(255,107,107,0.3); background:rgba(255,107,107,0.1);" onclick="deleteSocial('${soc.id}')">✕</button>
            </div>
            <label class="admin-checkbox" style="display:inline-flex;"><input type="checkbox" ${soc.visible ? 'checked' : ''} onchange="updateSocial('${soc.id}', 'visible', this.checked)"> Visible</label>
            <input type="text" class="admin-input" value="${soc.platform}" oninput="updateSocial('${soc.id}', 'platform', this.value)" placeholder="Plataforma (ej. YouTube)">
            <input type="text" class="admin-input" style="margin-bottom:0;" value="${soc.url}" oninput="updateSocial('${soc.id}', 'url', this.value)" placeholder="URL Completa">
          </div>
        `;
      });
      container.innerHTML = html;
    }

    function addSocial() {
        const id = 'soc_' + Date.now();
        const order = tempConfig.socials.length > 0 ? Math.max(...tempConfig.socials.map(s => s.order)) + 1 : 1;
        tempConfig.socials.push({ id, platform: 'Nueva Red', url: 'https://', visible: true, order });
        renderAdminSocialsList();
    }

    function updateSocial(id, field, value) {
        const s = tempConfig.socials.find(x => x.id === id);
        if(s) s[field] = value;
    }

    function deleteSocial(id) {
        if(confirm("¿Eliminar esta red social?")) {
            tempConfig.socials = tempConfig.socials.filter(x => x.id !== id);
            renderAdminSocialsList();
        }
    }

    function moveSocial(id, dir) {
        const idx = tempConfig.socials.findIndex(b => b.id === id);
        if (idx === -1) return;
        const targetIdx = idx + dir;
        if (targetIdx >= 0 && targetIdx < tempConfig.socials.length) {
            let temp = tempConfig.socials[idx].order;
            tempConfig.socials[idx].order = tempConfig.socials[targetIdx].order;
            tempConfig.socials[targetIdx].order = temp;
            tempConfig.socials.sort((a,b) => a.order - b.order);
            renderAdminSocialsList();
        }
    }

    function renderAdminCasesList() {
      const container = document.getElementById('adm-cases-list');
      let sorted = [...tempConfig.cases].sort((a,b) => (a.order||0) - (b.order||0));
      let html = '';
      sorted.forEach((c, idx) => {
        let isVis = c.visible !== false;
        html += `
          <div class="admin-group" style="position:relative; margin-bottom:15px;">
            <div style="position:absolute; top: 15px; right: 15px; display:flex; gap:5px; align-items:center;">
              <button class="admin-btn" onclick="moveCase(${c.id}, -1)" ${idx===0 ? 'disabled style="opacity:0.3"' : ''}>▲</button>
              <button class="admin-btn" onclick="moveCase(${c.id}, 1)" ${idx===sorted.length-1 ? 'disabled style="opacity:0.3"' : ''}>▼</button>
              <button class="admin-btn" style="color: #ff6b6b; border-color:rgba(255,107,107,0.3); background:rgba(255,107,107,0.1);" onclick="deleteCase(${c.id})">Borrar</button>
            </div>
            
            <div style="display:flex; align-items:center; gap: 15px; margin-bottom: 10px;">
                <label style="margin:0;">Caso #${idx+1}</label>
                <label class="admin-checkbox" style="margin:0;"><input type="checkbox" ${isVis ? 'checked' : ''} onchange="updateCase(${c.id}, 'visible', this.checked)"> Visible en web</label>
            </div>
            
            <input type="text" class="admin-input" value="${c.tag}" oninput="updateCase(${c.id}, 'tag', this.value)" placeholder="Etiqueta (ej. Derecho Penal)">
            <input type="text" class="admin-input" value="${c.title}" oninput="updateCase(${c.id}, 'title', this.value)" placeholder="Título del caso">
            
            <label style="margin-top:5px;">Imagen del Caso</label>
            <div style="display:flex; gap:10px; margin-bottom:10px;">
                <input type="text" class="admin-input" id="adm-case-img-${c.id}" style="margin-bottom:0;" value="${c.image}" oninput="updateCase(${c.id}, 'image', this.value)" placeholder="URL de la imagen">
                <button class="admin-btn-primary" id="btn-upload-case-${c.id}" onclick="document.getElementById('file-case-${c.id}').click()">SUBIR</button>
                <input type="file" id="file-case-${c.id}" hidden accept="image/*" onchange="uploadImage(this, 'adm-case-img-${c.id}', 'btn-upload-case-${c.id}')">
            </div>

            <textarea class="admin-input" style="min-height: 60px; resize:vertical;" oninput="updateCase(${c.id}, 'desc', this.value)" placeholder="Descripción...">${c.desc}</textarea>
          </div>
        `;
      });
      container.innerHTML = html;
    }

    function moveCase(id, dir) {
        const idx = tempConfig.cases.findIndex(b => b.id === id);
        if (idx === -1) return;
        const targetIdx = idx + dir;
        if (targetIdx >= 0 && targetIdx < tempConfig.cases.length) {
            let temp = tempConfig.cases[idx].order;
            tempConfig.cases[idx].order = tempConfig.cases[targetIdx].order;
            tempConfig.cases[targetIdx].order = temp;
            tempConfig.cases.sort((a,b) => (a.order||0) - (b.order||0));
            renderAdminCasesList();
        }
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
      const order = tempConfig.cases.length > 0 ? Math.max(...tempConfig.cases.map(x=>x.order||0)) + 1 : 1;
      tempConfig.cases.push({
        id: newId, tag: 'Nueva Área', title: 'Nuevo Caso', desc: 'Descripción del caso...', image: 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&q=80&w=400&h=200',
        visible: true, order: order
      });
      renderAdminCasesList();
    }

    function guardarAdmin() {
      tempConfig.header.title = document.getElementById('adm-title').value;
      tempConfig.header.showTitle = document.getElementById('adm-show-title').checked;
      tempConfig.header.subtitle = document.getElementById('adm-subtitle').value;
      tempConfig.header.showSubtitle = document.getElementById('adm-show-subtitle').checked;
      
      tempConfig.header.logo = document.getElementById('adm-logo').value;
      tempConfig.header.portrait = document.getElementById('adm-portrait').value;
      
      tempConfig.contact.whatsapp = document.getElementById('adm-whatsapp').value;
      tempConfig.contact.phone = document.getElementById('adm-phone').value;
      tempConfig.contact.email = document.getElementById('adm-email').value;
      tempConfig.contact.maps = document.getElementById('adm-maps').value;
      
      siteConfig = JSON.parse(JSON.stringify(tempConfig));
      localStorage.setItem('mpparra_config', JSON.stringify(siteConfig));
      
      renderApp();
      cerrarAdmin();
      showNotificationToast("Cambios guardados exitosamente");
    }
  </script>
"""
content = re.sub(r'<script>\s*let tempConfig = null;.*?guardarAdmin\(\) \{.*?</script>', lambda m: new_admin_js, content, flags=re.DOTALL)

with open('/Users/franmig33/Desktop/mpparra/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

