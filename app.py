import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILO COCA-COLA / REGINALD LEE
# ---------------------------------------------------------
st.set_page_config(
    page_title="Reginald Lee - Dashboard de Gastos",
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
    # Asegurar formato de fecha en MES
    if 'MES' in df.columns:
        df['MES_DT'] = pd.to_datetime(df['MES'])
        df['MES_NOMBRE'] = df['MES_DT'].dt.strftime('%Y-%m')
    return df

st.sidebar.header("⚙️ Carga de Base y Filtros")
uploaded_file = st.sidebar.file_uploader("Subir/Reemplazar Excel", type=["xlsx"])

df = None
if uploaded_file is not None:
    df = cargar_datos(uploaded_file)
else:
    try:
        df = cargar_datos("Base Dashboard.xlsx")
        st.sidebar.success("Base cargada desde el repositorio")
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

    # Separación Presupuesto vs Gasto Real
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
    # GRÁFICOS DINÁMICOS
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # GASTOS POR GRUPO DE CUENTAS
    # ---------------------------------------------------------
    st.subheader("Gasto Real por Grupo de Cuentas")
    g_grupo = gasto_df.groupby('GRUPO DE CUENTAS')['SALDO'].sum().reset_index().sort_values(by='SALDO', ascending=True)
    fig_grupo = px.bar(g_grupo, x='SALDO', y='GRUPO DE CUENTAS', orientation='h', color_discrete_sequence=['#E61C24'])
    fig_grupo.update_layout(template='plotly_white', xaxis_title="Monto ($)", yaxis_title="")
    st.plotly_chart(fig_grupo, use_container_width=True)

    # ---------------------------------------------------------
    # TABLA RESUMEN POR RESPONSABLE
    # ---------------------------------------------------------
    st.subheader("📋 Resumen por Responsable")
    p_resp = presupuesto_df.groupby('RESPONSABLE')['SALDO'].sum().rename('Presupuesto')
    g_resp = gasto_df.groupby('RESPONSABLE')['SALDO'].sum().rename('Gasto Real')
    tabla_resp = pd.concat([p_resp, g_resp], axis=1).fillna(0)
    tabla_resp['Desviación ($)'] = tabla_resp['Gasto Real'] - tabla_resp['Presupuesto']
    tabla_resp['% Ejecución'] = (tabla_resp['Gasto Real'] / tabla_resp['Presupuesto'] * 100).fillna(0)

    st.dataframe(
        tabla_resp.style.format({
            'Presupuesto': '$ {:,.0f}',
            'Gasto Real': '$ {:,.0f}',
            'Desviación ($)': '$ {:,.0f}',
            '% Ejecución': '{:.1f}%'
        }).background_gradient(subset=['Desviación ($)'], cmap='Reds'),
        use_container_width=True
    )