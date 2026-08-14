import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Dashboard de Gestión y Control Presupuestario",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuración por defecto para gráficos Plotly
PLOTLY_CONFIG = {'displayModeBar': False, 'responsive': True}

# ---------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (MODO OSCURO / PREMIUM)
# ---------------------------------------------------------
st.markdown("""
    <style>
        .main-header {
            background-color: #1E293B;
            padding: 1.2rem 1.5rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            border-left: 5px solid #E61C24;
        }
        .main-header h2 { color: #FFFFFF; margin: 0; font-size: 1.6rem; }
        .main-header p { color: #94A3B8; margin: 0.2rem 0 0 0; font-size: 0.95rem; }
        
        .custom-card {
            background-color: #1F2937;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #374151;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .card-title { color: #9CA3AF; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; }
        .card-value { color: #FFFFFF; font-size: 1.5rem; font-weight: 700; margin-top: 0.3rem; }
        
        .chart-box-title { 
            color: #FFFFFF; 
            font-weight: 600; 
            margin-bottom: 0.75rem; 
            font-size: 1rem;
            border-bottom: 1px solid #374151;
            padding-bottom: 0.4rem;
        }
        
        /* Ajuste de botón de borrado de filtros */
        .stButton>button {
            border-radius: 6px;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# FUNCIONES AUXILIARES Y DE BORRADO DE FILTROS
# ---------------------------------------------------------
def obtener_columna(df, candidatos):
    """Busca la primera columna coincidente dentro de una lista de candidatos."""
    if df is None or df.empty:
        return None
    for col in candidatos:
        if col in df.columns:
            return col
    return None

def formato_moneda(valor):
    """Formatea números a formato de moneda ($1.234.567)."""
    try:
        if pd.isna(valor):
            return "$0"
        return f"${valor:,.0f}".replace(",", ".")
    except:
        return "$0"

def limpiar_filtros():
    """Borra del session_state todas las claves de filtros aplicados."""
    keys_filtros = [
        # Módulo 1
        'f_resp_main', 'f_mes_main', 'f_cta_nom_main', 'search_main',
        # Módulo 2
        'f_resp_v', 'f_mes_v', 'f_cta_nom_v', 'search_v',
        # Módulo 3
        'f_resp_c', 'f_mes_c', 'f_cta_nom_c', 'search_c'
    ]
    for key in keys_filtros:
        if key in st.session_state:
            del st.session_state[key]

# ---------------------------------------------------------
# INICIALIZACIÓN DE ESTADO DE SESIÓN (SESSION STATE)
# ---------------------------------------------------------
if 'user' not in st.session_state:
    st.session_state['user'] = 'ADMIN'
if 'is_admin' not in st.session_state:
    st.session_state['is_admin'] = True

# Obtención de datos cargados previamente en la app principal
data_dict = st.session_state.get('data_dict', {})

# ---------------------------------------------------------
# NAVEGACIÓN Y BOTÓN LATERAL DE BORRADO DE FILTROS
# ---------------------------------------------------------
st.sidebar.title("📌 Menú Principal")
modulo_seleccionado = st.sidebar.radio(
    "Seleccione Módulo:",
    ["📊 Control Presupuestario", "🎟️ Vales de Consumo", "🛒 Compras"]
)

st.sidebar.markdown("---")

# Botón para la limpieza de filtros
if st.sidebar.button("🧹 Limpiar Todos los Filtros", use_container_width=True, type="secondary"):
    limpiar_filtros()
    st.rerun()

# ---------------------------------------------------------
# MÓDULO 1: CONTROL PRESUPUESTARIO
# ---------------------------------------------------------
if modulo_seleccionado == "📊 Control Presupuestario":
    st.markdown(f"""
        <div class="main-header">
            <h2>📊 Control y Seguimiento Presupuestario</h2>
            <p>Análisis Consolidado de Desviaciones y Ejecución | Usuario: <b>{st.session_state['user']}</b></p>
        </div>
    """, unsafe_allow_html=True)

    df_main = data_dict.get('main', pd.DataFrame())

    if df_main.empty:
        st.info("ℹ️ No se encontraron datos en la hoja principal. Por favor, asegúrese de haber cargado el archivo Excel correspondiente.")
    else:
        df_m_trabajo = df_main.copy()
        col_m_resp = 'RESPONSABLE' if 'RESPONSABLE' in df_m_trabajo.columns else obtener_columna(df_m_trabajo, ['USUARIO', 'RESPONSABLE_MAP'])
        col_m_mes = 'MES_NOMBRE' if 'MES_NOMBRE' in df_m_trabajo.columns else obtener_columna(df_m_trabajo, ['MES', 'FECHA'])
        col_m_nom_cta = obtener_columna(df_m_trabajo, ['DESC CTA CBLE', 'DESCRIPCION CUENTA', 'NOMBRE CUENTA', 'CUENTA_NORMALIZADA'])
        col_m_monto = obtener_columna(df_m_trabajo, ['REAL', 'EJECUTADO', 'MONTO', 'IMPORTE', 'ACTUAL'])

        # Filtrado por Admin / Usuario
        if not st.session_state['is_admin']:
            u_user = st.session_state['user'].upper()
            if col_m_resp and col_m_resp in df_m_trabajo.columns:
                df_m_user = df_m_trabajo[df_m_trabajo[col_m_resp].astype(str).str.upper() == u_user].copy()
            else:
                df_m_user = df_m_trabajo.copy()
        else:
            st.sidebar.subheader("🎯 Filtros Administrador")
            resps_disp = sorted(df_m_trabajo[col_m_resp].dropna().unique()) if col_m_resp in df_m_trabajo.columns else []
            f_resp_main = st.sidebar.multiselect("Filtrar por Responsables:", resps_disp, default=resps_disp, key="f_resp_main")
            
            if f_resp_main and col_m_resp in df_m_trabajo.columns:
                resps_upper = [r.upper() for r in f_resp_main]
                df_m_user = df_m_trabajo[df_m_trabajo[col_m_resp].astype(str).str.upper().isin(resps_upper)].copy()
            else:
                df_m_user = df_m_trabajo.copy()

        # Filtros laterales adicionales
        st.sidebar.subheader("🎯 Filtros Presupuesto")
        if col_m_mes and col_m_mes in df_m_user.columns:
            meses_m = sorted(df_m_user[col_m_mes].dropna().unique())
            f_mes_m = st.sidebar.multiselect("Filtrar Mes:", meses_m, default=meses_m, key="f_mes_main")
            if f_mes_m:
                df_m_user = df_m_user[df_m_user[col_m_mes].isin(f_mes_m)]

        if col_m_nom_cta and col_m_nom_cta in df_m_user.columns:
            ctas_m = sorted([str(c).strip() for c in df_m_user[col_m_nom_cta].dropna().unique() if str(c).strip() not in ['-', 'nan']])
            f_cta_nom_m = st.sidebar.multiselect("🔎 Filtrar Nombre de Cuenta Contable:", ctas_m, default=[], key="f_cta_nom_main")
            if f_cta_nom_m:
                df_m_user = df_m_user[df_m_user[col_m_nom_cta].astype(str).str.strip().isin(f_cta_nom_m)]

        # Métricas principales
        total_ejecutado = pd.to_numeric(df_m_user[col_m_monto], errors='coerce').sum() if col_m_monto else 0
        total_registros = len(df_m_user)

        km1, km2 = st.columns(2)
        with km1:
            st.markdown(f'<div class="custom-card"><div class="card-title">Monto Ejecutado Total</div><div class="card-value">{formato_moneda(total_ejecutado)}</div></div>', unsafe_allow_html=True)
        with km2:
            st.markdown(f'<div class="custom-card"><div class="card-title">Cuentas / Registros Evaluados</div><div class="card-value">{total_registros:,}</div></div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📋 Vista Detallada del Presupuesto")
        search_main = st.text_input("🔎 Buscar en el Presupuesto:", "", key="search_main")
        
        df_m_render = df_m_user.copy()
        if search_main:
            mask_m = df_m_render.astype(str).apply(lambda x: x.str.lower().str.contains(search_main.lower())).any(axis=1)
            df_m_render = df_m_render[mask_m]

        st.dataframe(df_m_render, use_container_width=True, height=380)

# ---------------------------------------------------------
# MÓDULO 2: VALES DE CONSUMO
# ---------------------------------------------------------
elif modulo_seleccionado == "🎟️ Vales de Consumo":
    st.markdown(f"""
        <div class="main-header">
            <h2>🎟️ Registro y Control de Vales de Consumo</h2>
            <p>Monitoreo de Salidas de Almacén y Consumos | Usuario: <b>{st.session_state['user']}</b></p>
        </div>
    """, unsafe_allow_html=True)

    df_main = data_dict.get('main', pd.DataFrame())
    df_vales = data_dict.get('vales', pd.DataFrame())

    if df_vales.empty:
        st.info("ℹ️ No se encontraron datos en la pestaña de 'Vales de Consumo'. Asegúrese de agregar la hoja correspondiente al Excel.")
    else:
        # 1. CRUCE LÓGICO DE INFORMACIÓN (MAIN <-> VALES)
        col_m_num_cta = obtener_columna(df_main, ['CUENTA', 'CTA CBLE', 'CUENTA CONTABLE', 'NRO CUENTA', 'CODIGO'])
        col_m_nom_cta = obtener_columna(df_main, ['DESC CTA CBLE', 'DESCRIPCION CUENTA', 'NOMBRE CUENTA', 'CUENTA_NORMALIZADA'])
        col_m_resp = 'RESPONSABLE'

        if col_m_num_cta and col_m_nom_cta and col_m_resp in df_main.columns:
            mapa_cuentas = df_main[[col_m_num_cta, col_m_nom_cta, col_m_resp]].drop_duplicates().copy()
            mapa_cuentas[col_m_num_cta] = mapa_cuentas[col_m_num_cta].astype(str).str.strip()
            mapa_cuentas[col_m_resp] = mapa_cuentas[col_m_resp].astype(str).str.strip().str.upper()
        else:
            mapa_cuentas = pd.DataFrame()

        col_v_num_cta = obtener_columna(df_vales, ['CUENTA', 'CTA CBLE', 'CUENTA CONTABLE', 'NRO CUENTA', 'CODIGO'])
        col_v_monto = obtener_columna(df_vales, ['MONTO', 'IMPORTE', 'TOTAL', 'SALDO', 'VALOR', 'PRECIO TOTAL', 'NETO'])
        col_v_mes = 'MES_NOMBRE' if 'MES_NOMBRE' in df_vales.columns else obtener_columna(df_vales, ['MES', 'FECHA'])

        df_v_trabajo = df_vales.copy()

        if col_v_num_cta and not mapa_cuentas.empty:
            df_v_trabajo['KEY_CTA'] = df_v_trabajo[col_v_num_cta].astype(str).str.strip()
            
            df_v_trabajo = df_v_trabajo.merge(
                mapa_cuentas.rename(columns={
                    col_m_num_cta: 'KEY_CTA',
                    col_m_nom_cta: 'NOMBRE_CUENTA_MAP',
                    col_m_resp: 'RESPONSABLE_MAP'
                }),
                on='KEY_CTA',
                how='left'
            )
            
            col_nombre_mostrar = 'NOMBRE_CUENTA_MAP'
            col_resp_cruce = 'RESPONSABLE_MAP'
        else:
            col_nombre_mostrar = obtener_columna(df_v_trabajo, ['DESC CTA CBLE', 'CONCEPTO', 'CATEGORIA', 'RUBRO'])
            col_resp_cruce = obtener_columna(df_v_trabajo, ['RESPONSABLE', 'USUARIO', 'RETIRA'])

        # 2. FILTRADO POR RESPONSABLE LOGUEADO
        if not st.session_state['is_admin']:
            u_user = st.session_state['user'].upper()
            if col_resp_cruce in df_v_trabajo.columns:
                df_v_user = df_v_trabajo[df_v_trabajo[col_resp_cruce].astype(str).str.upper() == u_user].copy()
            else:
                df_v_user = df_v_trabajo.copy()
        else:
            st.sidebar.subheader("🎯 Filtros Administrador")
            resps_disp = sorted(df_main['RESPONSABLE'].dropna().unique()) if not df_main.empty and 'RESPONSABLE' in df_main.columns else []
            f_resp_v = st.sidebar.multiselect("Filtrar por Responsables:", resps_disp, default=resps_disp, key="f_resp_v")
            
            if f_resp_v and col_resp_cruce in df_v_trabajo.columns:
                resps_upper = [r.upper() for r in f_resp_v]
                df_v_user = df_v_trabajo[df_v_trabajo[col_resp_cruce].astype(str).str.upper().isin(resps_upper)].copy()
            else:
                df_v_user = df_v_trabajo.copy()

        # 3. FILTROS LATERALES
        st.sidebar.subheader("🎯 Filtros Vales de Consumo")
        
        if col_v_mes and col_v_mes in df_v_user.columns:
            meses_v = sorted(df_v_user[col_v_mes].dropna().unique())
            f_mes_v = st.sidebar.multiselect("Filtrar Mes:", meses_v, default=meses_v, key="f_mes_v")
            if f_mes_v:
                df_v_user = df_v_user[df_v_user[col_v_mes].isin(f_mes_v)]

        if col_nombre_mostrar and col_nombre_mostrar in df_v_user.columns:
            nombres_cuentas_unicas = sorted(
                [str(c).strip() for c in df_v_user[col_nombre_mostrar].dropna().unique() if str(c).strip() not in ['-', 'nan']]
            )
            f_cta_nom_v = st.sidebar.multiselect("🔎 Filtrar Nombre de Cuenta Contable:", nombres_cuentas_unicas, default=[], key="f_cta_nom_v")
            if f_cta_nom_v:
                df_v_user = df_v_user[df_v_user[col_nombre_mostrar].astype(str).str.strip().isin(f_cta_nom_v)]

        # 4. MÉTRICAS Y GRÁFICOS OPTIMIZADOS
        col_vg1, col_vg2 = st.columns([1.2, 1.1])
        
        with col_vg1:
            st.markdown('<div class="chart-box-title">📦 Top 5 Artículos más Consumidos</div>', unsafe_allow_html=True)
            col_v_art = obtener_columna(df_v_user, ['ARTICULO', 'ARTÍCULO', 'DESCRIPCION', 'DESCRIPCIÓN', 'DESCRIPCION LARGA', 'PRODUCTO', 'DETALLE'])
            
            if col_v_art and col_v_monto and col_v_art in df_v_user.columns:
                df_v_user[col_v_monto] = pd.to_numeric(df_v_user[col_v_monto], errors='coerce').fillna(0)
                
                g_art_v = df_v_user.groupby(col_v_art)[col_v_monto].apply(lambda x: abs(x.sum())).reset_index()
                g_art_v = g_art_v.sort_values(by=col_v_monto, ascending=True).tail(5)

                fig_art_v = px.bar(
                    g_art_v, 
                    x=col_v_monto, 
                    y=col_v_art, 
                    orientation='h',
                    color_discrete_sequence=['#E61C24']
                )
                
                fig_art_v.update_xaxes(title="", tickformat="$,.0f")
                fig_art_v.update_yaxes(title="")
                fig_art_v.update_traces(hovertemplate='<b>Artículo:</b> %{y}<br><b>Monto Consumido:</b> $%{x:,.0f}')
                
                fig_art_v.update_layout(
                    autosize=True, paper_bgcolor='#1F2937', plot_bgcolor='#1F2937', font=dict(color='#FFFFFF'),
                    height=300, margin=dict(l=15, r=15, t=15, b=25)
                )
                st.plotly_chart(fig_art_v, use_container_width=True, config=PLOTLY_CONFIG)
            else:
                st.info("ℹ️ No se detectó la columna de Artículos o Detalle en la hoja de Vales.")

        with col_vg2:
            st.markdown('<div class="chart-box-title">📊 Distribución por Nombre de Cuenta</div>', unsafe_allow_html=True)
            if col_nombre_mostrar and col_v_monto and col_nombre_mostrar in df_v_user.columns:
                df_v_user[col_v_monto] = pd.to_numeric(df_v_user[col_v_monto], errors='coerce').fillna(0)
                
                g_cta_v = df_v_user.groupby(col_nombre_mostrar)[col_v_monto].apply(lambda x: abs(x.sum())).reset_index()
                total_monto = g_cta_v[col_v_monto].sum()

                if total_monto > 0:
                    g_cta_v['PCT'] = (g_cta_v[col_v_monto] / total_monto) * 100
                    principales = g_cta_v[g_cta_v['PCT'] >= 2.0].copy()
                    otros_monto = g_cta_v[g_cta_v['PCT'] < 2.0][col_v_monto].sum()

                    if otros_monto > 0:
                        fila_otros = pd.DataFrame([{col_nombre_mostrar: 'OTROS CONSUMOS', col_v_monto: otros_monto, 'PCT': (otros_monto/total_monto)*100}])
                        g_cta_v = pd.concat([principales, fila_otros], ignore_index=True)
                    else:
                        g_cta_v = principales
                
                g_cta_v = g_cta_v.sort_values(by=col_v_monto, ascending=False)
                
                fig_cv = px.pie(
                    g_cta_v, 
                    values=col_v_monto, 
                    names=col_nombre_mostrar, 
                    hole=0.45, 
                    color_discrete_sequence=['#E61C24', '#4B5563', '#9CA3AF', '#374151', '#D1D5DB']
                )
                
                fig_cv.update_traces(
                    textposition='inside', 
                    textinfo='percent',
                    hovertemplate='<b>%{label}</b><br>Monto: $%{value:,.0f}<br>Porcentaje: %{percent}'
                )
                
                fig_cv.update_layout(
                    autosize=True, paper_bgcolor='#1F2937', plot_bgcolor='#1F2937', font=dict(color='#FFFFFF'),
                    height=300, margin=dict(l=15, r=15, t=10, b=45),
                    legend=dict(
                        orientation="h",
                        y=-0.2,
                        x=0,
                        font=dict(color='#FFFFFF', size=11)
                    )
                )
                st.plotly_chart(fig_cv, use_container_width=True, config=PLOTLY_CONFIG)

        # 5. TABLA GENERAL
        st.markdown("---")
        st.markdown("### 📋 Registro Detallado de Vales de Consumo")

        search_v = st.text_input("🔎 Buscar por Nombre de Cuenta, Artículos o Detalles:", "", key="search_v")
        
        cols_ocultar = ['KEY_CTA', 'RESPONSABLE_MAP']
        df_v_render = df_v_user.drop(columns=[c for c in cols_ocultar if c in df_v_user.columns]).copy()

        if search_v:
            mask_v = df_v_render.astype(str).apply(lambda x: x.str.lower().str.contains(search_v.lower())).any(axis=1)
            df_v_render = df_v_render[mask_v]

        st.dataframe(df_v_render, use_container_width=True, height=380)

# ---------------------------------------------------------
# MÓDULO 3: COMPRAS
# ---------------------------------------------------------
elif modulo_seleccionado == "🛒 Compras":
    st.markdown(f"""
        <div class="main-header">
            <h2>🛒 Registro y Control de Compras</h2>
            <p>Gestión de Órdenes y Proveedores | Usuario: <b>{st.session_state['user']}</b></p>
        </div>
    """, unsafe_allow_html=True)

    df_main = data_dict.get('main', pd.DataFrame())
    df_compras = data_dict.get('compras', pd.DataFrame())

    if df_compras.empty:
        st.info("ℹ️ No se encontraron datos en la pestaña de 'Compras'. Asegúrese de agregar la hoja correspondiente al Excel.")
    else:
        # 1. CRUCE LÓGICO DE INFORMACIÓN (MAIN <-> COMPRAS)
        col_m_num_cta = obtener_columna(df_main, ['CUENTA', 'CTA CBLE', 'CUENTA CONTABLE', 'NRO CUENTA', 'CODIGO'])
        col_m_nom_cta = obtener_columna(df_main, ['DESC CTA CBLE', 'DESCRIPCION CUENTA', 'NOMBRE CUENTA', 'CUENTA_NORMALIZADA'])
        col_m_resp = 'RESPONSABLE'

        if col_m_num_cta and col_m_nom_cta and col_m_resp in df_main.columns:
            mapa_cuentas = df_main[[col_m_num_cta, col_m_nom_cta, col_m_resp]].drop_duplicates().copy()
            mapa_cuentas[col_m_num_cta] = mapa_cuentas[col_m_num_cta].astype(str).str.strip()
            mapa_cuentas[col_m_resp] = mapa_cuentas[col_m_resp].astype(str).str.strip().str.upper()
        else:
            mapa_cuentas = pd.DataFrame()

        col_c_num_cta = obtener_columna(df_compras, ['CUENTA', 'CTA CBLE', 'CUENTA CONTABLE', 'NRO CUENTA', 'CODIGO'])
        col_c_monto = obtener_columna(df_compras, ['MONTO', 'IMPORTE', 'TOTAL', 'SALDO', 'VALOR', 'PRECIO TOTAL', 'NETO_TOTAL_FACTURA', 'PRECIO', 'NETO'])
        col_c_mes = 'MES_NOMBRE' if 'MES_NOMBRE' in df_compras.columns else obtener_columna(df_compras, ['MES', 'FECHA'])

        df_c_trabajo = df_compras.copy()

        if col_c_num_cta and not mapa_cuentas.empty:
            df_c_trabajo['KEY_CTA'] = df_c_trabajo[col_c_num_cta].astype(str).str.strip()
            
            df_c_trabajo = df_c_trabajo.merge(
                mapa_cuentas.rename(columns={
                    col_m_num_cta: 'KEY_CTA',
                    col_m_nom_cta: 'NOMBRE_CUENTA_MAP',
                    col_m_resp: 'RESPONSABLE_MAP'
                }),
                on='KEY_CTA',
                how='left'
            )
            
            col_nombre_mostrar = 'NOMBRE_CUENTA_MAP'
            col_resp_cruce = 'RESPONSABLE_MAP'
        else:
            col_nombre_mostrar = obtener_columna(df_c_trabajo, ['DESC CTA CBLE', 'CONCEPTO', 'CATEGORIA', 'RUBRO', 'PROVEEDOR'])
            col_resp_cruce = obtener_columna(df_c_trabajo, ['RESPONSABLE', 'USUARIO', 'SOLICITANTE'])

        # 2. FILTRADO POR RESPONSABLE LOGUEADO
        if not st.session_state['is_admin']:
            u_user = st.session_state['user'].upper()
            if col_resp_cruce in df_c_trabajo.columns:
                df_c_user = df_c_trabajo[df_c_trabajo[col_resp_cruce].astype(str).str.upper() == u_user].copy()
            else:
                df_c_user = df_c_trabajo.copy()
        else:
            st.sidebar.subheader("🎯 Filtros Administrador")
            resps_disp = sorted(df_main['RESPONSABLE'].dropna().unique()) if not df_main.empty and 'RESPONSABLE' in df_main.columns else []
            f_resp_c = st.sidebar.multiselect("Filtrar por Responsables:", resps_disp, default=resps_disp, key="f_resp_c")
            
            if f_resp_c and col_resp_cruce in df_c_trabajo.columns:
                resps_upper = [r.upper() for r in f_resp_c]
                df_c_user = df_c_trabajo[df_c_trabajo[col_resp_cruce].astype(str).str.upper().isin(resps_upper)].copy()
            else:
                df_c_user = df_c_trabajo.copy()

        # 3. FILTROS LATERALES
        st.sidebar.subheader("🎯 Filtros Compras")
        
        if col_c_mes and col_c_mes in df_c_user.columns:
            meses_c = sorted(df_c_user[col_c_mes].dropna().unique())
            f_mes_c = st.sidebar.multiselect("Filtrar Mes:", meses_c, default=meses_c, key="f_mes_c")
            if f_mes_c:
                df_c_user = df_c_user[df_c_user[col_c_mes].isin(f_mes_c)]

        if col_nombre_mostrar and col_nombre_mostrar in df_c_user.columns:
            nombres_cuentas_unicas = sorted(
                [str(c).strip() for c in df_c_user[col_nombre_mostrar].dropna().unique() if str(c).strip() not in ['-', 'nan']]
            )
            f_cta_nom_c = st.sidebar.multiselect("🔎 Filtrar Nombre de Cuenta Contable:", nombres_cuentas_unicas, default=[], key="f_cta_nom_c")
            if f_cta_nom_c:
                df_c_user = df_c_user[df_c_user[col_nombre_mostrar].astype(str).str.strip().isin(f_cta_nom_c)]

        # 4. MÉTRICAS Y GRÁFICOS OPTIMIZADOS
        compras_totales = len(df_c_user)
        monto_total_c = abs(pd.to_numeric(df_c_user[col_c_monto], errors='coerce').sum()) if col_c_monto else 0
        promedio_compra = (monto_total_c / compras_totales) if compras_totales > 0 else 0

        kc1, kc2, kc3 = st.columns(3)
        with kc1:
            st.markdown(f'<div class="custom-card"><div class="card-title">Monto Total Compras</div><div class="card-value">{formato_moneda(monto_total_c)}</div></div>', unsafe_allow_html=True)
        with kc2:
            st.markdown(f'<div class="custom-card"><div class="card-title">Cantidad de Registros</div><div class="card-value">{compras_totales:,}</div></div>', unsafe_allow_html=True)
        with kc3:
            st.markdown(f'<div class="custom-card"><div class="card-title">Promedio por Registro</div><div class="card-value">{formato_moneda(promedio_compra)}</div></div>', unsafe_allow_html=True)

        col_cg1, col_cg2 = st.columns([1.2, 1.1])
        
        with col_cg1:
            st.markdown('<div class="chart-box-title">🏢 Top 5 Proveedores más Solicitados</div>', unsafe_allow_html=True)
            col_c_prov = obtener_columna(df_c_user, ['RAZ_SOCIAL', 'RAZON SOCIAL', 'RAZÓN SOCIAL', 'NOMBRE PROVEEDOR', 'NOMBRE_PROVEEDOR'])
            
            if col_c_prov and col_c_monto and col_c_prov in df_c_user.columns:
                df_c_user[col_c_monto] = pd.to_numeric(df_c_user[col_c_monto], errors='coerce').fillna(0)
                
                df_c_user['PROVEEDOR_LABEL'] = df_c_user[col_c_prov].astype(str).str.strip()
                df_c_clean = df_c_user[~df_c_user['PROVEEDOR_LABEL'].isin(['nan', 'None', '', '0', '-', 'NAN'])].copy()

                g_prov_c = df_c_clean.groupby('PROVEEDOR_LABEL')[col_c_monto].apply(lambda x: abs(x.sum())).reset_index()
                g_prov_c = g_prov_c.sort_values(by=col_c_monto, ascending=True).tail(5)

                fig_prov_c = px.bar(
                    g_prov_c, 
                    x=col_c_monto, 
                    y='PROVEEDOR_LABEL', 
                    orientation='h',
                    color_discrete_sequence=['#E61C24']
                )
                
                fig_prov_c.update_xaxes(title="", tickformat="$,.0f")
                fig_prov_c.update_yaxes(type='category', title="")
                fig_prov_c.update_traces(hovertemplate='<b>Proveedor:</b> %{y}<br><b>Monto Comprado:</b> $%{x:,.0f}')
                
                fig_prov_c.update_layout(
                    autosize=True, paper_bgcolor='#1F2937', plot_bgcolor='#1F2937', font=dict(color='#FFFFFF'),
                    height=300, margin=dict(l=15, r=15, t=15, b=25)
                )
                st.plotly_chart(fig_prov_c, use_container_width=True, config=PLOTLY_CONFIG)
            else:
                st.info("ℹ️ No se detectó la columna RAZ_SOCIAL en la hoja de Compras.")

        with col_cg2:
            st.markdown('<div class="chart-box-title">📊 Distribución por Nombre de Cuenta</div>', unsafe_allow_html=True)
            if col_nombre_mostrar and col_c_monto and col_nombre_mostrar in df_c_user.columns:
                df_c_user[col_c_monto] = pd.to_numeric(df_c_user[col_c_monto], errors='coerce').fillna(0)
                
                g_cta_c = df_c_user.groupby(col_nombre_mostrar)[col_c_monto].apply(lambda x: abs(x.sum())).reset_index()
                total_monto_c = g_cta_c[col_c_monto].sum()

                if total_monto_c > 0:
                    g_cta_c['PCT'] = (g_cta_c[col_c_monto] / total_monto_c) * 100
                    principales_c = g_cta_c[g_cta_c['PCT'] >= 2.0].copy()
                    otros_monto_c = g_cta_c[g_cta_c['PCT'] < 2.0][col_c_monto].sum()

                    if otros_monto_c > 0:
                        fila_otros = pd.DataFrame([{col_nombre_mostrar: 'OTRAS COMPRAS', col_c_monto: otros_monto_c, 'PCT': (otros_monto_c/total_monto_c)*100}])
                        g_cta_c = pd.concat([principales_c, fila_otros], ignore_index=True)
                    else:
                        g_cta_c = principales_c
                
                g_cta_c = g_cta_c.sort_values(by=col_c_monto, ascending=False)
                
                fig_cc = px.pie(
                    g_cta_c, 
                    values=col_c_monto, 
                    names=col_nombre_mostrar, 
                    hole=0.45, 
                    color_discrete_sequence=['#E61C24', '#4B5563', '#9CA3AF', '#374151', '#D1D5DB']
                )
                
                fig_cc.update_traces(
                    textposition='inside', 
                    textinfo='percent',
                    hovertemplate='<b>%{label}</b><br>Monto: $%{value:,.0f}<br>Porcentaje: %{percent}'
                )
                
                fig_cc.update_layout(
                    autosize=True, paper_bgcolor='#1F2937', plot_bgcolor='#1F2937', font=dict(color='#FFFFFF'),
                    height=300, margin=dict(l=15, r=15, t=10, b=45),
                    legend=dict(
                        orientation="h",
                        y=-0.2,
                        x=0,
                        font=dict(color='#FFFFFF', size=11)
                    )
                )
                st.plotly_chart(fig_cc, use_container_width=True, config=PLOTLY_CONFIG)

        # 5. TABLA GENERAL
        st.markdown("---")
        st.markdown("### 📋 Registro Detallado de Compras")

        search_c = st.text_input("🔎 Buscar por Nombre de Cuenta, Proveedor o Detalles:", "", key="search_c")
        
        cols_ocultar_c = ['KEY_CTA', 'RESPONSABLE_MAP', 'PROVEEDOR_LABEL']
        df_c_render = df_c_user.drop(columns=[c for c in cols_ocultar_c if c in df_c_user.columns]).copy()

        if search_c:
            mask_c = df_c_render.astype(str).apply(lambda x: x.str.lower().str.contains(search_c.lower())).any(axis=1)
            df_c_render = df_c_render[mask_c]

        st.dataframe(df_c_render, use_container_width=True, height=380)
