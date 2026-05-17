import re

with open('/Users/franmig33/Desktop/mpparra/index.html', 'r') as f:
    content = f.read()

# 1. Add admin styles
admin_styles = """
    /* ==========================================================================
       12. ESTILOS DE ADMINISTRACIÓN (NO EXPORTABLES)
       ========================================================================== */
    <style id="admin-styles">
        .admin-lock-btn {
            position: fixed; bottom: 10px; right: 10px; width: 32px; height: 32px;
            opacity: 0.1; z-index: 99999; cursor: pointer; color: #fff;
            display: flex; align-items: center; justify-content: center; transition: opacity 0.3s;
        }
        .admin-lock-btn:hover { opacity: 0.8; }
        
        #admin-panel-wrapper {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(10,11,13,0.85); backdrop-filter: blur(10px);
            z-index: 9999999; display: flex; justify-content: flex-end;
            opacity: 0; pointer-events: none; transition: opacity 0.4s ease;
            font-family: 'Montserrat', sans-serif;
        }
        #admin-panel-wrapper.active { opacity: 1; pointer-events: auto; }
        
        #admin-pane {
            width: 100%; max-width: 420px; height: 100%; background: #111317;
            border-left: 1px solid var(--gold-primary); display: flex; flex-direction: column;
            box-shadow: -10px 0 30px rgba(0,0,0,0.8);
            transform: translateX(100%); transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }
        #admin-panel-wrapper.active #admin-pane { transform: translateX(0); }
        
        .admin-header {
            padding: 20px 24px; background: #0a0b0d; border-bottom: 1px solid rgba(223, 186, 107, 0.3);
            display: flex; justify-content: space-between; align-items: center;
        }
        .admin-header h2 { font-family: 'Cinzel', serif; font-size: 16px; color: var(--gold-primary); font-weight: 700; letter-spacing: 1px;}
        .admin-close { background: none; border: none; color: white; cursor: pointer; display: flex; }
        .admin-close:hover { color: var(--gold-primary); }
        
        .admin-body { flex-grow: 1; overflow-y: auto; padding: 20px 24px; }
        .admin-body::-webkit-scrollbar { width: 4px; }
        .admin-body::-webkit-scrollbar-thumb { background: var(--gold-dark); border-radius: 4px; }
        
        .admin-section { margin-bottom: 30px; }
        .admin-section h3 { font-size: 11px; color: var(--gold-primary); margin-bottom: 15px; text-transform: uppercase; letter-spacing: 2px; border-bottom: 1px solid rgba(223,186,107,0.1); padding-bottom: 8px;}
        
        .admin-field { margin-bottom: 15px; }
        .admin-field label { display: block; font-size: 10px; margin-bottom: 6px; color: var(--text-gray); text-transform: uppercase; letter-spacing: 1px;}
        .admin-field input[type="text"], .admin-field textarea {
            width: 100%; padding: 10px 12px; background: #0a0b0d; border: 1px solid rgba(223, 186, 107, 0.2);
            color: white; border-radius: 8px; font-family: inherit; font-size: 12px; transition: border-color 0.3s;
        }
        .admin-field input:focus, .admin-field textarea:focus { border-color: var(--gold-primary); outline: none; }
        .admin-field textarea { resize: vertical; min-height: 60px; }
        
        .admin-checkbox { display: flex; align-items: center; gap: 8px; font-size: 11px; margin-bottom: 15px; color: #fff; cursor: pointer;}
        
        .admin-btn {
            background: rgba(223, 186, 107, 0.1); color: var(--gold-primary); border: 1px solid var(--gold-primary); padding: 10px 15px;
            border-radius: 8px; font-weight: 600; cursor: pointer; width: 100%; font-size: 10px; text-transform: uppercase; letter-spacing: 1px;
            transition: all 0.3s; display: flex; align-items: center; justify-content: center; gap: 8px;
        }
        .admin-btn:hover { background: var(--gold-primary); color: #0a0b0d; }
        .admin-btn-secondary { background: transparent; border-color: #333; color: #a4b0be; }
        .admin-btn-secondary:hover { background: #333; color: white; border-color: #555;}
        
        .admin-list-item {
            background: rgba(255,255,255,0.02); border: 1px solid rgba(223,186,107,0.15); padding: 12px; margin-bottom: 12px; border-radius: 8px;
        }
        .admin-list-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .admin-list-title { font-size: 11px; font-weight: 600; color: #fff;}
        .admin-list-actions { display: flex; gap: 6px; }
        .admin-icon-btn { background: #1a1c20; border: 1px solid #333; color: #a4b0be; cursor: pointer; width: 24px; height: 24px; border-radius: 4px; display: flex; align-items: center; justify-content: center; transition: all 0.2s;}
        .admin-icon-btn:hover { background: var(--gold-primary); color: black; border-color: var(--gold-primary); }
        .admin-icon-btn svg { width: 12px; height: 12px; }
        
        .export-zone { padding: 20px 24px; background: #0a0b0d; border-top: 1px solid var(--gold-primary); }
        .export-btn { background: var(--gold-gradient); color: #000; border: none; font-weight: 700; box-shadow: 0 4px 15px rgba(223,186,107,0.2);}
        .export-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(223,186,107,0.4); }
        .export-desc { font-size: 9px; color: var(--text-gray); text-align: center; margin-top: 10px; line-height: 1.4;}
    </style>
"""

content = content.replace('</style>', '</style>\n' + admin_styles)

# 2. Add State Script
state_script = """
    <!-- ==========================================================================
       ESTADO CENTRALIZADO (SITE_CONFIG) - SE ACTUALIZA AL EXPORTAR
       ========================================================================== -->
    <script id="state-script">
        window.SITE_CONFIG = {
            header: {
                showTitle: true,
                titleText: "MP PARRA & ASOCIADOS",
                showSubtitle: true,
                subtitleText: "Estudio Jurídico & Estrategia Pública",
                logoUrl: "https://res.cloudinary.com/drpuhj6mc/image/upload/v1779039483/LOGO_rjejdk.jpg"
            },
            profile: {
                portraitUrl: "image_4493e7.jpg"
            },
            contact: {
                email: "contacto@mpparra.com",
                phone: "+593 99 451 1585"
            },
            buttons: [
                { id: 'whatsapp', type: 'whatsapp', label: 'Mensaje', url: 'https://wa.me/593994511585', visible: true, order: 1 },
                { id: 'phone', type: 'phone', label: 'Teléfono', url: 'tel:+593994511585', visible: true, order: 2 },
                { id: 'email', type: 'email', label: 'E-Mail', url: '', visible: true, order: 3 },
                { id: 'social', type: 'social', label: 'Red Social', url: 'https://instagram.com', visible: true, order: 4 },
                { id: 'location', type: 'location', label: 'Localización', url: 'https://maps.google.com', visible: true, order: 5 }
            ],
            cases: [
                { id: 1, tag: 'Derecho Corporativo', title: 'Reestructuración Empresarial', desc: 'Asesoría jurídica integral en fusiones, adquisiciones y reestructuración de pasivos para grandes consorcios nacionales y multinacionales.', image: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&q=80&w=400&h=200' },
                { id: 2, tag: 'Estrategia Pública', title: 'Contratación & Políticas Públicas', desc: 'Consultoría estratégica y representación legal de alta complejidad ante entidades reguladoras y contratación estatal de infraestructura.', image: 'https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&q=80&w=400&h=200' },
                { id: 3, tag: 'Litigio Premium', title: 'Defensa Tributaria & Financiera', desc: 'Defensa ante controversias fiscales de alta cuantía, logrando resoluciones favorables ante la administración pública y tribunales.', image: 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&q=80&w=400&h=200' }
            ]
        };
    </script>
"""

content = content.replace('<script>', state_script + '\n    <script id="main-script">')

# 3. Update variables in JS
content = re.sub(r'const EMAIL_DATA = ".*?";', 'const EMAIL_DATA = window.SITE_CONFIG.contact.email;', content)
content = re.sub(r'const PHONE_DATA = ".*?";', 'const PHONE_DATA = window.SITE_CONFIG.contact.phone;', content)

# 4. Modify HTML IDs for dynamic rendering
content = re.sub(r'<div class="firm-title-text">.*?</div>', '<div class="firm-title-text" id="render-firm-title"></div>', content)
content = re.sub(r'<div class="firm-subtitle-text">.*?</div>', '<div class="firm-subtitle-text" id="render-firm-subtitle"></div>', content)

# 5. Clear buttons grid and cases list
content = re.sub(r'<div class="grid-row-triple">.*?</div>\s*<!-- Fila de 2 Botones -->\s*<div class="grid-row-double">.*?</div>', 
                 '<div id="render-action-links"></div>', content, flags=re.DOTALL)

content = re.sub(r'<div class="gallery-modal-body">.*?</div>', 
                 '<div class="gallery-modal-body" id="render-cases-list"></div>', content, flags=re.DOTALL)

# 6. Add render functions to JS
render_js = """
        // ==========================================================================
        // MOTOR DE RENDERIZADO DINÁMICO
        // ==========================================================================
        function renderApp() {
            const config = window.SITE_CONFIG;
            
            // Textos
            const titleEl = document.getElementById('render-firm-title');
            if (titleEl) {
                titleEl.innerText = config.header.titleText;
                titleEl.style.display = config.header.showTitle ? 'block' : 'none';
            }
            
            const subtitleEl = document.getElementById('render-firm-subtitle');
            if (subtitleEl) {
                subtitleEl.innerText = config.header.subtitleText;
                subtitleEl.style.display = config.header.showSubtitle ? 'block' : 'none';
            }
            
            // Imágenes
            const logoEl = document.getElementById('logoElement');
            if (logoEl && config.header.logoUrl) logoEl.src = config.header.logoUrl;
            
            const portraitEl = document.getElementById('portraitElement');
            if (portraitEl && config.profile.portraitUrl) portraitEl.src = config.profile.portraitUrl;
            
            // Render Botones (3 arriba, resto abajo)
            const linksContainer = document.getElementById('render-action-links');
            if (linksContainer) {
                let sortedBtns = [...config.buttons].filter(b => b.visible).sort((a,b) => a.order - b.order);
                let html = '<div class="grid-row-triple">';
                let inDouble = false;
                
                sortedBtns.forEach((btn, index) => {
                    if (index === 3 && !inDouble) {
                        html += '</div><div class="grid-row-double">';
                        inDouble = true;
                    }
                    
                    let svgIcon = '';
                    let actionAttr = '';
                    
                    if (btn.type === 'whatsapp') {
                        svgIcon = '<svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z"/></svg>';
                        actionAttr = `href="${btn.url}" target="_blank" onclick="alertConexion('${btn.label}')"`;
                    } else if (btn.type === 'phone') {
                        svgIcon = '<svg viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>';
                        actionAttr = `href="${btn.url}" onclick="alertConexion('${btn.label}')"`;
                    } else if (btn.type === 'email') {
                        svgIcon = '<svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>';
                        actionAttr = `href="#" onclick="copiarEmail(event)"`;
                    } else if (btn.type === 'social') {
                        svgIcon = '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3.2"/><path d="M9 2h6c3.87 0 7 3.13 7 7v6c0 3.87-3.13 7-7 7H9c-3.87 0-7-3.13-7-7V9c0-3.87 3.13-7 7-7zm0 1.5c-3.03 0-5.5 2.47-5.5 5.5v6c0 3.03 2.47 5.5 5.5 5.5h6c3.03 0 5.5-2.47 5.5-5.5V9c0-3.03-2.47-5.5-5.5-5.5H9zM18.5 4.5a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>';
                        actionAttr = `href="${btn.url}" target="_blank" onclick="alertConexion('${btn.label}')"`;
                    } else if (btn.type === 'location') {
                        svgIcon = '<svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>';
                        actionAttr = `href="${btn.url}" target="_blank" onclick="alertConexion('${btn.label}')"`;
                    }
                    
                    const tag = btn.type === 'email' ? 'button' : 'a';
                    const closing = btn.type === 'email' ? '</button>' : '</a>';
                    
                    html += `
                        <${tag} ${actionAttr} class="btn-card-action">
                            <div class="icon-gold-ring">${svgIcon}</div>
                            <span class="label-enmarcada">${btn.label}</span>
                        ${closing}
                    `;
                });
                html += '</div>'; // close last row
                linksContainer.innerHTML = html;
            }
            
            // Render Casos
            const casesContainer = document.getElementById('render-cases-list');
            if (casesContainer) {
                let html = '';
                config.cases.forEach(c => {
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
                    </div>`;
                });
                casesContainer.innerHTML = html;
            }
        }
        
        window.addEventListener('DOMContentLoaded', () => {
            renderApp();
        });
"""

content = content.replace('window.addEventListener(\'DOMContentLoaded\', () => {', render_js + '\n        window.addEventListener(\'DOMContentLoaded\', () => {')


# 7. Add Admin DOM and JS at the end
admin_html = """
    <!-- Sutil Candado -->
    <div class="admin-lock-btn" id="admin-lock-trigger" onclick="abrirAdmin()">
        <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
    </div>

    <!-- Panel de Administración -->
    <div id="admin-panel-wrapper">
        <div id="admin-pane">
            <div class="admin-header">
                <h2>Tablero de Control</h2>
                <button class="admin-close" onclick="cerrarAdmin()">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
            </div>
            
            <div class="admin-body">
                
                <div class="admin-section">
                    <h3>Cabecera</h3>
                    <label class="admin-checkbox">
                        <input type="checkbox" id="adm-show-title" onchange="updateConfig()"> Mostrar Título
                    </label>
                    <div class="admin-field">
                        <input type="text" id="adm-title" oninput="updateConfig()" placeholder="Título Principal">
                    </div>
                    <label class="admin-checkbox">
                        <input type="checkbox" id="adm-show-subtitle" onchange="updateConfig()"> Mostrar Subtítulo
                    </label>
                    <div class="admin-field">
                        <input type="text" id="adm-subtitle" oninput="updateConfig()" placeholder="Subtítulo">
                    </div>
                </div>

                <div class="admin-section">
                    <h3>Imágenes (URLs)</h3>
                    <div class="admin-field">
                        <label>Logo (Recomendado: Cloudinary)</label>
                        <input type="text" id="adm-logo" oninput="updateConfig()" placeholder="URL del Logo">
                    </div>
                    <div class="admin-field">
                        <label>Retrato</label>
                        <input type="text" id="adm-portrait" oninput="updateConfig()" placeholder="URL del Retrato">
                    </div>
                </div>

                <div class="admin-section">
                    <h3>Contacto General</h3>
                    <div class="admin-field">
                        <label>Correo Electrónico (VCard & Copiar)</label>
                        <input type="text" id="adm-email" oninput="updateConfig()">
                    </div>
                    <div class="admin-field">
                        <label>Teléfono Base (VCard)</label>
                        <input type="text" id="adm-phone" oninput="updateConfig()">
                    </div>
                </div>

                <div class="admin-section">
                    <h3>Botones de Acción</h3>
                    <div id="adm-buttons-list"></div>
                </div>

                <div class="admin-section">
                    <h3>Casos de Éxito</h3>
                    <div id="adm-cases-list"></div>
                    <button class="admin-btn" onclick="addCase()">+ Añadir Nuevo Caso</button>
                </div>

            </div>
            
            <div class="export-zone">
                <button class="admin-btn export-btn" onclick="exportarLimpio()">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                    Exportar Código Limpio
                </button>
                <div class="export-desc">Descarga tu tarjeta final y súbela a Netlify. El candado y el panel desaparecerán mágicamente.</div>
            </div>
        </div>
    </div>

    <script id="admin-logic">
        const ADMIN_PASS = "admin123";

        function abrirAdmin() {
            const pass = prompt("Ingrese la contraseña de Administrador:");
            if (pass === ADMIN_PASS) {
                document.getElementById('admin-panel-wrapper').classList.add('active');
                populateAdmin();
            } else if (pass !== null) {
                alert("Contraseña incorrecta.");
            }
        }

        function cerrarAdmin() {
            document.getElementById('admin-panel-wrapper').classList.remove('active');
        }

        function populateAdmin() {
            const c = window.SITE_CONFIG;
            document.getElementById('adm-show-title').checked = c.header.showTitle;
            document.getElementById('adm-title').value = c.header.titleText;
            document.getElementById('adm-show-subtitle').checked = c.header.showSubtitle;
            document.getElementById('adm-subtitle').value = c.header.subtitleText;
            document.getElementById('adm-logo').value = c.header.logoUrl;
            document.getElementById('adm-portrait').value = c.profile.portraitUrl;
            document.getElementById('adm-email').value = c.contact.email;
            document.getElementById('adm-phone').value = c.contact.phone;
            
            renderAdminButtons();
            renderAdminCases();
        }

        function updateConfig() {
            const c = window.SITE_CONFIG;
            c.header.showTitle = document.getElementById('adm-show-title').checked;
            c.header.titleText = document.getElementById('adm-title').value;
            c.header.showSubtitle = document.getElementById('adm-show-subtitle').checked;
            c.header.subtitleText = document.getElementById('adm-subtitle').value;
            c.header.logoUrl = document.getElementById('adm-logo').value;
            c.profile.portraitUrl = document.getElementById('adm-portrait').value;
            c.contact.email = document.getElementById('adm-email').value;
            c.contact.phone = document.getElementById('adm-phone').value;
            
            renderApp();
        }

        function renderAdminButtons() {
            const list = document.getElementById('adm-buttons-list');
            let html = '';
            let sorted = [...window.SITE_CONFIG.buttons].sort((a,b) => a.order - b.order);
            
            sorted.forEach((btn, index) => {
                html += `
                <div class="admin-list-item">
                    <div class="admin-list-header">
                        <label class="admin-checkbox" style="margin:0;"><input type="checkbox" ${btn.visible ? 'checked' : ''} onchange="updateBtnVis('${btn.id}', this.checked)"> ${btn.label}</label>
                        <div class="admin-list-actions">
                            <button class="admin-icon-btn" onclick="moveBtn('${btn.id}', -1)" title="Subir" ${index===0 ? 'disabled style="opacity:0.3"' : ''}>▲</button>
                            <button class="admin-icon-btn" onclick="moveBtn('${btn.id}', 1)" title="Bajar" ${index===sorted.length-1 ? 'disabled style="opacity:0.3"' : ''}>▼</button>
                        </div>
                    </div>
                    ${btn.type !== 'email' ? `<div class="admin-field" style="margin-bottom:0;"><input type="text" value="${btn.url}" oninput="updateBtnUrl('${btn.id}', this.value)" placeholder="URL destino"></div>` : ''}
                </div>`;
            });
            list.innerHTML = html;
        }

        function updateBtnVis(id, visible) {
            const btn = window.SITE_CONFIG.buttons.find(b => b.id === id);
            if (btn) btn.visible = visible;
            renderApp();
        }

        function updateBtnUrl(id, url) {
            const btn = window.SITE_CONFIG.buttons.find(b => b.id === id);
            if (btn) btn.url = url;
            renderApp();
        }

        function moveBtn(id, dir) {
            const btns = window.SITE_CONFIG.buttons;
            const idx = btns.findIndex(b => b.id === id);
            if (idx === -1) return;
            
            const targetIdx = idx + dir;
            if (targetIdx >= 0 && targetIdx < btns.length) {
                // Swap orders
                const temp = btns[idx].order;
                btns[idx].order = btns[targetIdx].order;
                btns[targetIdx].order = temp;
                btns.sort((a,b) => a.order - b.order);
                renderAdminButtons();
                renderApp();
            }
        }

        // Casos Logic
        function renderAdminCases() {
            const list = document.getElementById('adm-cases-list');
            let html = '';
            window.SITE_CONFIG.cases.forEach((c, idx) => {
                html += `
                <div class="admin-list-item">
                    <div class="admin-list-header">
                        <span class="admin-list-title">Caso #${idx+1}</span>
                        <button class="admin-icon-btn" onclick="deleteCase(${c.id})" style="background:rgba(200,50,50,0.2); border-color:rgba(200,50,50,0.5); color:#ff6b6b;" title="Borrar">✕</button>
                    </div>
                    <div class="admin-field"><label>Etiqueta</label><input type="text" value="${c.tag}" oninput="updateCase(${c.id}, 'tag', this.value)"></div>
                    <div class="admin-field"><label>Título</label><input type="text" value="${c.title}" oninput="updateCase(${c.id}, 'title', this.value)"></div>
                    <div class="admin-field"><label>Descripción</label><textarea oninput="updateCase(${c.id}, 'desc', this.value)">${c.desc}</textarea></div>
                    <div class="admin-field" style="margin-bottom:0;"><label>URL Imagen</label><input type="text" value="${c.image}" oninput="updateCase(${c.id}, 'image', this.value)"></div>
                </div>`;
            });
            list.innerHTML = html;
        }

        function updateCase(id, field, value) {
            const c = window.SITE_CONFIG.cases.find(x => x.id === id);
            if (c) c[field] = value;
            renderApp();
        }

        function deleteCase(id) {
            if(confirm("¿Seguro que deseas borrar este caso?")) {
                window.SITE_CONFIG.cases = window.SITE_CONFIG.cases.filter(x => x.id !== id);
                renderAdminCases();
                renderApp();
            }
        }

        function addCase() {
            const newId = window.SITE_CONFIG.cases.length > 0 ? Math.max(...window.SITE_CONFIG.cases.map(c=>c.id)) + 1 : 1;
            window.SITE_CONFIG.cases.push({
                id: newId, tag: 'Nueva Área', title: 'Nuevo Caso de Éxito', desc: 'Descripción breve de este caso.', image: 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&q=80&w=400&h=200'
            });
            renderAdminCases();
            renderApp();
        }

        // ==========================================================================
        // EXPORTADOR INTELIGENTE
        // ==========================================================================
        function exportarLimpio() {
            // 1. Clonar DOM
            const docClone = document.documentElement.cloneNode(true);
            
            // 2. Limpiar rastros administrativos
            const elementsToRemove = [
                '#admin-styles', 
                '#admin-lock-trigger', 
                '#admin-panel-wrapper', 
                '#admin-logic'
            ];
            elementsToRemove.forEach(sel => {
                const el = docClone.querySelector(sel);
                if (el) el.remove();
            });

            // 3. Serializar estado e inyectar en el clon
            const stateScript = docClone.querySelector('#state-script');
            if (stateScript) {
                const cleanState = JSON.stringify(window.SITE_CONFIG, null, 4);
                stateScript.innerHTML = `\\n        window.SITE_CONFIG = ${cleanState};\\n    `;
            }

            // 4. Formatear y descargar
            const cleanHTML = '<!DOCTYPE html>\\n<html lang="es">\\n' + docClone.innerHTML + '\\n</html>';
            const blob = new Blob([cleanHTML], { type: 'text/html;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            
            const link = document.createElement('a');
            link.download = 'index.html';
            link.href = url;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            cerrarAdmin();
            setTimeout(() => {
                showNotificationToast("Exportación exitosa. ¡Listo para Netlify!");
            }, 500);
        }
    </script>
</body>
"""

content = content.replace('</body>', admin_html)

with open('/Users/franmig33/Desktop/mpparra/index.html', 'w') as f:
    f.write(content)

