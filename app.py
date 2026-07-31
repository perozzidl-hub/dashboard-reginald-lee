import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILO COCA-COLA / REGINALD LEE
# ---------------------------------------------------------
st.set_page_config(
    page_title="Reginald Lee - Control Presupuestario y Gastos",
    page_icon="🥤",
    layout="wide"
)

# Estilo visual corporativo (Rojo Coca-Cola #E61C24 y Gris Oscuro #1E1E1E)
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    h1, h2, h3 { color: #E61C24 !important; font-family: 'Helvetica Neue', Arial, sans-serif; }
    div[data-testid="stMetricValue"] { font-size: 26px; color: #1E1E1E; font-weight: bold; }
    .stMultiSelect label, .stSelectbox label { font-weight: bold; color: #1E1E1E; }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 16px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Control de Presupuesto y Gastos Fijos")
st.caption("Reginald Lee S.A. — Embotellador Oficial de Coca-Cola")
st.markdown("---")

# ---------------------------------------------------------
# CARGA Y PROCESAMIENTO DE DATOS
# ---------------------------------------------------------
@st.cache_data
def cargar_datos(file):
    df = pd.read_excel(file)
    if 'MES' in df.columns:
        df['MES_DT'] = pd.to_datetime(df['MES'])
        df['MES_NOMBRE'] = df['MES_DT'].dt.strftime('%Y-%m')
    
    # Rellenar valores nulos para columnas textuales
    cols_texto = ['INTERNO', 'DES1', 'DES2', 'TEXTO INTERNO', 'DESC CTA CBLE', 'RAZON', 'COMPROBANTE', 'ORDEN DE COMPRA']
    for c in cols_texto:
        if c in df.columns:
            df[c] = df[c].fillna('-')
            
    return df

st.sidebar.header("⚙️ Filtros de Control")
uploaded_file = st.sidebar.file_uploader("Subir / Reemplazar Excel", type=["xlsx"])

df = None
if uploaded_file is not None:
    df = cargar_datos(uploaded_file)
else:
    try:
        df = cargar_datos("Base Dashboard.xlsx")
        st.sidebar.success("Base 'Base Dashboard.xlsx' activa")
    except Exception:
        st.info("👆 Por favor sube el archivo 'Base Dashboard.xlsx' en el panel lateral.")

if df is not None:
    # ---------------------------------------------------------
    # FILTROS DINÁMICOS
    # ---------------------------------------------------------
    meses = sorted(df['MES_NOMBRE'].dropna().unique())
    locaciones = sorted(df['LOCACION'].dropna().unique())
    responsables = sorted(df['RESPONSABLE'].dropna().unique())
    grupos = sorted(df['GRUPO DE CUENTAS'].dropna().unique())

    f_mes = st.sidebar.multiselect("Seleccionar Meses", meses, default=meses)
    f_loc = st.sidebar.multiselect("Locación / Planta", locaciones, default=locaciones)
    f_resp = st.sidebar.multiselect("Responsable", responsables, default=responsables)
    f_grupo = st.sidebar.multiselect("Grupo de Cuentas", grupos, default=grupos)

    # Filtrar Dataset
    df_filtrado = df[
        (df['MES_NOMBRE'].isin(f_mes)) &
        (df['LOCACION'].isin(f_loc)) &
        (df['RESPONSABLE'].isin(f_resp)) &
        (df['GRUPO DE CUENTAS'].isin(f_grupo))
    ]

    presupuesto_df = df_filtrado[df_filtrado['TIPO2'] == 'PRESUPUESTO']
    gasto_df = df_filtrado[df_filtrado['TIPO2'] == 'GASTO']

    tot_presupuesto = presupuesto_df['SALDO'].sum()
    tot_gasto = gasto_df['SALDO'].sum()
    desviacion = tot_gasto - tot_presupuesto
    pct_ejecucion = (tot_gasto / tot_presupuesto * 100) if tot_presupuesto > 0 else 0

    # ---------------------------------------------------------
    # METRICAS PRINCIPALES (KPIs)
    # ---------------------------------------------------------
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Presupuesto Total", f"$ {tot_presupuesto:,.0f}")
    kpi2.metric("Gasto Real Total", f"$ {tot_gasto:,.0f}")
    kpi3.metric("Desviación ($)", f"$ {desviacion:,.0f}", delta=f"$ {desviacion:,.0f}", delta_color="inverse")
    kpi4.metric("% Ejecución Presupuestaria", f"{pct_ejecucion:.1f}%")

    st.markdown("---")

    # ---------------------------------------------------------
    # ESTRUCTURA EN PESTAÑAS (TABS)
    # ---------------------------------------------------------
    tab1, tab2, tab3 = st.tabs(["📊 Visión General", "🔍 Auditoría de Gastos (Detalle)", "📌 Resumen por Cuentas"])

    # ---------------------------------------------------------
    # TAB 1: VISIÓN GENERAL
    # ---------------------------------------------------------
    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Evolución Mensual: Presupuesto vs Gasto")
            p_mes = presupuesto_df.groupby('MES_NOMBRE')['SALDO'].sum().reset_index().rename(columns={'SALDO': 'Presupuesto'})
            g_mes = gasto_df.groupby('MES_NOMBRE')['SALDO'].sum().reset_index().rename(columns={'SALDO': 'Gasto Real'})
            comp_mes = pd.merge(p_mes, g_mes, on='MES_NOMBRE', how='outer').fillna(0)

            fig_mes = go.Figure()
            fig_mes.add_trace(go.Bar(x=comp_mes['MES_NOMBRE'], y=comp_mes['Presupuesto'], name='Presupuesto', marker_color='#1E1E1E'))
            fig_mes.add_trace(go.Bar(x=comp_mes['MES_NOMBRE'], y=comp_mes['Gasto Real'], name='Gasto Real', marker_color='#E61C24'))
            fig_mes.update_layout(barmode='group', template='plotly_white', margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig_mes, use_container_width=True)

        with col2:
            st.subheader("Distribución del Gasto Real por Locación")
            g_loc = gasto_df.groupby('LOCACION')['SALDO'].sum().reset_index()
            fig_loc = px.pie(
                g_loc, values='SALDO', names='LOCACION',
                color_discrete_sequence=['#E61C24', '#1E1E1E', '#7F1D1D', '#9CA3AF', '#D1D5DB', '#4B5563', '#374151']
            )
            fig_loc.update_traces(textposition='inside', textinfo='percent+label')
            fig_loc.update_layout(margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig_loc, use_container_width=True)

        st.subheader("Gasto Real por Grupo de Cuentas")
        g_grupo = gasto_df.groupby('GRUPO DE CUENTAS')['SALDO'].sum().reset_index().sort_values(by='SALDO', ascending=True)
        fig_grupo = px.bar(g_grupo, x='SALDO', y='GRUPO DE CUENTAS', orientation='h', color_discrete_sequence=['#E61C24'])
        fig_grupo.update_layout(template='plotly_white', xaxis_title="Monto ($)", yaxis_title="")
        st.plotly_chart(fig_grupo, use_container_width=True)

    # ---------------------------------------------------------
    # TAB 2: AUDITORÍA DE GASTOS CON DETALLE
    # ---------------------------------------------------------
    with tab2:
        st.subheader("🔍 Detalle Transaccional de Gastos Registrados")
        st.caption("Filtra y explora las transacciones individuales con sus proveedores, descripciones e identificadores internos.")

        # Buscador de texto libre para auditoría
        search_term = st.text_input("🔎 Buscar por Proveedor (DES1), N° Interno, Texto o Comprobante:", "")

        df_gasto_detalle = gasto_df.copy()

        if search_term:
            s = search_term.lower()
            mask = (
                df_gasto_detalle['DES1'].astype(str).str.lower().str.contains(s) |
                df_gasto_detalle['INTERNO'].astype(str).str.lower().str.contains(s) |
                df_gasto_detalle['TEXTO INTERNO'].astype(str).str.lower().str.contains(s) |
                df_gasto_detalle['DESC CTA CBLE'].astype(str).str.lower().str.contains(s) |
                df_gasto_detalle['COMPROBANTE'].astype(str).str.lower().str.contains(s)
            )
            df_gasto_detalle = df_gasto_detalle[mask]

        # Selección de columnas clave a mostrar
        cols_mostrar = [
            'FECHA', 'MES_NOMBRE', 'LOCACION', 'RESPONSABLE', 
            'GRUPO DE CUENTAS', 'DESC CTA CBLE', 'DES1', 
            'TEXTO INTERNO', 'INTERNO', 'COMPROBANTE', 'SALDO'
        ]
        
        # Renombrar para mejor lectura en pantalla
        df_display = df_gasto_detalle[cols_mostrar].rename(columns={
            'MES_NOMBRE': 'MES',
            'DESC CTA CBLE': 'CUENTA CONTABLE',
            'DES1': 'PROVEEDOR / ENTIDAD',
            'TEXTO INTERNO': 'DESCRIPCIÓN INTERNA',
            'INTERNO': 'N° INTERNO',
            'SALDO': 'MONTO ($)'
        })

        st.markdown(f"**Registros encontrados:** {len(df_display):,} transacciones | **Monto Acumulado:** $ {df_display['MONTO ($)'].sum():,.0f}")

        st.dataframe(
            df_display.style.format({
                'MONTO ($)': '$ {:,.2f}'
            }),
            use_container_width=True,
            height=450
        )

    # ---------------------------------------------------------
    # TAB 3: RESUMEN POR CUENTAS Y RESPONSABLE
    # ---------------------------------------------------------
    with tab3:
        st.subheader("📌 Análisis Comparativo por Cuenta Contable")
        
        p_cta = presupuesto_df.groupby(['GRUPO DE CUENTAS', 'DESC CTA CBLE'])['SALDO'].sum().rename('Presupuesto')
        g_cta = gasto_df.groupby(['GRUPO DE CUENTAS', 'DESC CTA CBLE'])['SALDO'].sum().rename('Gasto Real')
        
        tabla_cta = pd.concat([p_cta, g_cta], axis=1).fillna(0).reset_index()
        tabla_cta['Desviación ($)'] = tabla_cta['Gasto Real'] - tabla_cta['Presupuesto']
        tabla_cta['% Ejecución'] = (tabla_cta['Gasto Real'] / tabla_cta['Presupuesto'] * 100).fillna(0)
        
        tabla_cta = tabla_cta.rename(columns={
            'GRUPO DE CUENTAS': 'GRUPO',
            'DESC CTA CBLE': 'CUENTA CONTABLE'
        }).sort_values(by='Desviación ($)', ascending=False)

        st.dataframe(
            tabla_cta.style.format({
                'Presupuesto': '$ {:,.0f}',
                'Gasto Real': '$ {:,.0f}',
                'Desviación ($)': '$ {:,.0f}',
                '% Ejecución': '{:.1f}%'
            }),
            use_container_width=True,
            height=450
        )
