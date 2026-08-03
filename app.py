import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Reginald Lee - Dashboard Presupuestario",
    page_icon="🍾",
    layout="wide",
    initial_sidebar_state="auto"
)

# Logo de Coca-Cola en Base64 para garantizar que cargue sin fallas de ruta
COCA_COLA_LOGO = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAG4AAAC8CAYAAACw6sBvAAAACXBIWXMAAAsTAAALEwEAmpwYAAAgAElEQVR4nOy9d5xdZ3X3/1376fObOn1GM6j3Zkuy3KtyL7gh/4mNqTbgAiSQGDC9BEgIJAECpACvMZiYYA/uDXchS7as3p/pffq5/f2j21caC+Mk92f23q+fDzq3nrLPee21n73X3uuvI4312dr6jNf/6A18tsb/y9i/S0e1/3L9Gf7/I52pByip9Ym3j3/Iew3yW/5pIes1xP121E/0L3+/a3qO/k3364f9bC/S12d8T5v3/WwtP4v+1+Ea70eIez56S24/c1r85f/3k//xH/5903e1eU//S+f+/1q9jI41Efcjrf3d80O98eG650I0/P8yS/1a/W841f3iP1e3/9eR2l7+D/pCjY3yR9e0T8j//A3274S2D/lPjG/12L/E3/9/m1/9AfxX//N3A6y1//Oa2p/oQ9r/T7o/734d/2Uf+z/iXp/6xIer3/P923/6n2l4LqL//6p3L4f/8O/507A+7Pvei3uT//07x/+y10y4j2e97+s4e1a+/bAfl3vT7E8o439s41m/54dr+o4f36v/v15a6eFqf6Tf5p5/4sM8/M+557/m7+i53/I//49/+3j/Aze/3f/+/3X4Rj9/qX4r4//P66eL+8p8n//m3/328m894T4m/S97/Z++p/aX4A/78z89u/9L/O9fIn3/N8T/Jvd+xP39/P2vj/z/L/v03/2x/u//h+O/+kG254/S6+83mO0H/77332/0833299/S8Z92y//O1v9//+O/hR/9R/rA/2I//4XN/m//tP/7a//0a9/x34I91///39Gv+2L/9X/8Xf2+L/8f8v1eN313+/2H68D25/3/P9P18+/5O8T4t///m1/+A/7/77z/A2P/lH4Xf8/H//S/+wG254/S68v/zP6/1/X1/6O/+iC+/X8P//0D9s8b2+v//f/sX98S6f/sF/9Sj//3H//9j/77s2792wX+S2N3+/X/+Hj/qX5L6+/iX//f1+/m/z//4l9s6199f/L2u1f3T+6d/j5X+L/o+p98X6z/f+z9/q+352d++z/1fS/+7+0n5Jv/yN3/0/m3Xy57/eL/03xR/x/v3L/yX/+s6e0z34L//v7/s/eO93e504c4I7X4I08C///Pj9m/3e9z24//76P///7//x/n/q3838384w4743/p99787/03/46r23/n/+h8//88A983+5/y1/8M75P3yU38/u585//e77/5f5/5/i///2//473v/38Xyv//f/3/+d8+/9f/+v/sP8f8n//r/s3/+sI4/2p/i/iO4/y/n8A/019P+S+p7/f//5/y/i3//1f6l99m9/89s6+s9L/oP799824X8f237+/u//+9/3p/3e52/vj+uD9O3/yA58b/30D3//hA98y7+4v/7/5n+vX4sS1/71/qf31XwD76/g/bN/p5/vJv5H4v9/+sM02131I3e3t3e/+aD3/09/x/y///j4B8x4s4X433X90m/s6L0s//2M+4D/z458v3v155/O4r5/2e/v/1e6u2b+67/o3e/mD5s6N4v//40z1x6o5/u1y6S73/r/+N/1f4P/+/8O//x/m17+99/a//l//3a/m538P3X/r+7e1A4y3w4w42/c4f2vG6S8j4i8m5N2+y81e4b/4f/7b2z64m22//2o/d1z0m/i32w799/98b//uF8c//P4p4N/78f8v9yL22x4z6f/c3+4/+r/r80+/0+c8X5P7fS/9R/f5f1x11/5u//39P37X5vNfX7A3O8xS3l34//g8752203/j7uM8v0S/uB/f1sP13+3f//5S34v1i6R3q6S3y4UaXv93p9u7N+cT5e4j84U6v2w5f1jH2t6/25+O/rX8fS/050f249l6d/2p2831/+z//xI8Y3y5S2O9I/5A3a9H/aP+p/a9S8d58p4q/+s6pP1r+uN3vT6O2f09/2/hH+9uX3i+22Xp4f2q8p7sN/3j409O2v3i4f1+L4482f5v/+X/+o4/2y13t8p2x1+L4S7k0Lq127+7t2/+dG+a+Z1x559e2Z351v55s21//v02/+f2l3y+d3zXv+tE93x741x8G0//f+7L4eS9339a/+X1+v526S5763r//S7uT8R3+n3e3//f5u/v2f2sP//5S3+/838n/i15e/oP/1q8O//w7q2x+i2L1v/4E/8d6x0+f9N//h3Ovd/7v/2D9s/eL//s3e1P//Gf4E16i5n47/+19/6+0v7X2v3n/sN6+8v4m+P7bO39a95//X3P86d5e5m4s4z6f12y///zE3f8l/zN//41i8o/3i///0233b37n4N/l7e5i/3t35s1f1f/o+/qB6I31a98vI+d11397s4q7S3/4n43/8P5I6y/u3/aA3961///016d4g4b73+U/+a4E6y4L4D+/d05//+G2/7e9w+/v/3/iX6X/q63qA7eA1/uH3jvv99w2///fO5P8Dff+n//v8m//9//A3mO8oD1x7x335r5v819y+/i/38f0e/37j4E97/239+s3/2a1a8c1//y/04P//j5P+E++8d//9N12239+v1v+577y4m/5/v/jO0/e9N+n24/3x/+31/o6m3+/c1/231///+n+e8o3y29v/z858R4T+mP2L/tL9//0S9/n3/xTz5a8c11y14/+88w4X5H/v//8//A1m8//e39lX4n6w7//mX52t799/m/w5eO+/X/x8e1v8U/1/32u1+/f3f4e3mP4w6s7u2f0d90v8v5/b04G7236d8m///P5Xy+j/S/1L/92x5w7/5m///eS++2l/S5X4q5e44G59//uO212///gL/2i1/+b/8A/t/w7/u++8zX+5j9e3e3sS9a7u5s3t35s1f1e+/uJ2f52v/xR2z/q8D/0s4d242636L///6P+f+2A59k6///uG/3j//7Dff8s3//G/8//v8y76d47y5K4715r531P+f//A0x6g352/+2X/+l+eS///k///64f6+X+E2Xp5L7wz38q7e9A2d9x/0z/oD/67/y8/9aP/1/p5n/2P3+38w/+e4E+z8d3++8l5M/+pL9l3f2/+g53wO232N8wO9A0u/f259q3e56t3l4W/+o4f7e52+v8uP/m6v//+/191///543/S08e5v9q6r+S//42///r7/X2///A5b9e0I1/5wz//a7e87X9z//D3/4f7/h8N7jff/q+x6v3f114h/q724v0d77//q6p/21/i1335q4518//w6m/8d+j3///w=="


st.markdown(f"""
    <style>
    .stApp {{
        background-color: #F8F9FA !important;
    }}

    /* ------------------------------------
       LOGIN SIMÉTRICO Y ELEGANTE
    ------------------------------------ */
    .login-header-box {{
        text-align: center;
        margin-bottom: 20px;
    }}
    
    .coca-cola-logo {{
        width: 48px;
        height: auto;
        margin-bottom: 8px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }}

    .login-title {{
        color: #111827 !important;
        font-weight: 800 !important;
        font-size: 24px !important;
        margin-top: 4px !important;
        margin-bottom: 2px !important;
        letter-spacing: -0.5px;
    }}

    .login-subtitle {{
        color: #6B7280 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }}

    /* Tarjeta del Formulario */
    div[data-testid="stForm"] {{
        background-color: #FFFFFF !important;
        border-radius: 16px !important;
        padding: 32px 28px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.07) !important;
        border-top: 5px solid #E61C24 !important;
        border-left: 1px solid #E5E7EB !important;
        border-right: 1px solid #E5E7EB !important;
        border-bottom: 1px solid #E5E7EB !important;
        max-width: 420px;
        margin: 0 auto;
    }}

    div[data-testid="stForm"] label {{
        color: #1F2937 !important;
        font-weight: 700 !important;
        font-size: 13px !important;
    }}

    /* Inputs Limpios */
    div[data-testid="stForm"] input {{
        background-color: #F9FAFB !important;
        color: #111827 !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
    }}

    div[data-testid="stForm"] input:focus {{
        border-color: #E61C24 !important;
        box-shadow: 0 0 0 3px rgba(230, 28, 36, 0.15) !important;
    }}

    div[data-testid="stForm"] div[data-baseweb="input"] {{
        background-color: #F9FAFB !important;
        border-radius: 8px !important;
    }}

    /* Botón Submit */
    div[data-testid="stForm"] button[kind="secondaryFormSubmit"] {{
        background-color: #E61C24 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 11px 20px !important;
        width: 100% !important;
        margin-top: 15px !important;
        transition: all 0.2s ease !important;
    }}

    div[data-testid="stForm"] button[kind="secondaryFormSubmit"]:hover {{
        background-color: #C81018 !important;
        box-shadow: 0 4px 12px rgba(230, 28, 36, 0.3) !important;
    }}

    /* ------------------------------------
       BARRA LATERAL Y DASHBOARD
    ------------------------------------ */
    section[data-testid="stSidebar"] {{
        background-color: #111827 !important;
    }}
    
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] h4, 
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {{
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }}

    .main h1, .main h2, .main h3, .main h4, .main h5,
    div[data-testid="stMarkdownContainer"] h3,
    div[data-testid="stMarkdownContainer"] h4 {{
        color: #111827 !important;
        font-weight: 700 !important;
    }}

    .main-header {{
        background: linear-gradient(135deg, #111111 0%, #E61C24 100%);
        padding: 20px 25px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(230, 28, 36, 0.2);
    }}
    .main-header h2 {{
        color: #FFFFFF !important;
        margin: 0;
        font-weight: 800;
        font-size: 24px;
    }}
    .main-header p {{
        margin-top: 5px;
        color: #F3F4F6 !important;
        font-size: 13px;
        margin-bottom: 0;
    }}

    .custom-card {{
        background-color: #FFFFFF;
        border-radius: 12px !important;
        padding: 18px 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-top: 4px solid #E61C24;
        margin-bottom: 15px;
        min-height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
    .card-title {{
        font-size: 12px;
        font-weight: 700;
        color: #4B5563 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }}
    .card-value {{
        font-size: 20px;
        font-weight: 800;
        color: #111827 !important;
        margin-bottom: 2px;
    }}
    .card-sub {{
        font-size: 11px;
        font-weight: 600;
    }}
    .text-red {{ color: #E61C24 !important; }}
    .text-green {{ color: #10B981 !important; }}

    div[data-testid="stPlotlyChart"] {{
        background-color: #111827 !important;
        border-radius: 14px !important;
        padding: 10px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
        overflow: hidden !important;
    }}

    .detail-popup {{
        background-color: #FEF3C7 !important;
        border-left: 6px solid #D97706 !important;
        padding: 18px 22px !important;
        border-radius: 12px !important;
        margin: 15px 0 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
    }}
    .detail-popup h5 {{
        color: #B45309 !important;
        font-weight: 800 !important;
        margin: 0 0 10px 0 !important;
        font-size: 16px !important;
    }}
    .detail-popup p {{
        font-size: 15px !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        margin: 0 !important;
        line-height: 1.5 !important;
    }}
    .detail-popup small {{
        color: #374151 !important;
        font-size: 12px !important;
        font-weight: 600 !important;
    }}
    .detail-popup hr {{
        margin: 12px 0 !important;
        border-color: #FCD34D !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# FUNCIONES AUXILIARES
# ---------------------------------------------------------
def formato_moneda(valor, con_decimales=False):
    if pd.isna(valor):
        return "$ 0"
    if con_decimales:
        res = f"{valor:,.2f}"
    else:
        res = f"{valor:,.0f}"
    return "$ " + res.replace(',', 'X').replace('.', ',').replace('X', '.')

# ---------------------------------------------------------
# CARGA DE DATOS
# ---------------------------------------------------------
@st.cache_data
def cargar_datos(file):
    df = pd.read_excel(file)
    if 'MES' in df.columns:
        df['MES_DT'] = pd.to_datetime(df['MES'])
        df['MES_NOMBRE'] = df['MES_DT'].dt.strftime('%Y-%m')
    
    cols_texto = ['INTERNO', 'DES1', 'DES2', 'TEXTO INTERNO', 'DESC CTA CBLE', 'RAZON', 'COMPROBANTE']
    for c in cols_texto:
        if c in df.columns:
            df[c] = df[c].fillna('-')
            
    return df

@st.cache_data
def obtener_base_inicial():
    try:
        return cargar_datos("Base Dashboard.xlsx")
    except Exception:
        return None

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = None
if 'is_admin' not in st.session_state:
    st.session_state['is_admin'] = False
if 'df_data' not in st.session_state:
    st.session_state['df_data'] = obtener_base_inicial()

# ---------------------------------------------------------
# LOGIN CON BOTELLA Y DISEÑO SIMÉTRICO
# ---------------------------------------------------------
if not st.session_state['logged_in']:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
    
    with col_l2:
        with st.form("login_form"):
            st.markdown(f"""
                <div class="login-header-box">
                    <img src="{COCA_COLA_LOGO}" class="coca-cola-logo" alt="Coca Cola Logo"/>
                    <div class="login-title">Reginald Lee S.A.</div>
                    <div class="login-subtitle">Plataforma de Control Presupuestario</div>
                </div>
            """, unsafe_allow_html=True)
            
            user_input = st.text_input("Usuario (Responsable)", placeholder="Ej: galdeman o admin").strip()
            pass_input = st.text_input("Contraseña", type="password").strip()
            submit_login = st.form_submit_button("🔑 Ingresar al Dashboard")
            
            if submit_login:
                if user_input and pass_input:
                    df_temp = st.session_state['df_data']
                    
                    if user_input.lower() == "admin" and pass_input == "admin@":
                        st.session_state['logged_in'] = True
                        st.session_state['user'] = "ADMINISTRADOR"
                        st.session_state['is_admin'] = True
                        st.rerun()
                    elif df_temp is not None:
                        responsables = [str(r).upper() for r in df_temp['RESPONSABLE'].dropna().unique()]
                        u_upper = user_input.upper()
                        pass_esperado = user_input.lower() + "@"
                        
                        if u_upper in responsables and pass_input == pass_esperado:
                            st.session_state['logged_in'] = True
                            st.session_state['user'] = u_upper
                            st.session_state['is_admin'] = False
                            st.rerun()
                        else:
                            st.error("❌ Credenciales inválidas.")
                    else:
                        st.error("⚠️ Base de datos no disponible.")
                else:
                    st.warning("Ingrese usuario y contraseña.")
    st.stop()

# ---------------------------------------------------------
# MAIN DASHBOARD
# ---------------------------------------------------------
df = st.session_state['df_data']

# Sidebar
st.sidebar.markdown(f"👤 **Usuario Activo:** `{st.session_state['user']}`")
if st.session_state['is_admin']:
    st.sidebar.caption("🔑 Perfil: Administrador General")
else:
    st.sidebar.caption("📊 Perfil: Responsable de Sector")

if st.sidebar.button("🚪 Cerrar Sesión"):
    st.session_state['logged_in'] = False
    st.session_state['user'] = None
    st.session_state['is_admin'] = False
    st.rerun()

st.sidebar.markdown("---")

if st.session_state['is_admin']:
    st.sidebar.subheader("📤 Actualizar Base de Datos")
    new_file = st.sidebar.file_uploader("Subir Excel Principal", type=["xlsx"])
    if new_file is not None:
        st.session_state['df_data'] = cargar_datos(new_file)
        df = st.session_state['df_data']
        st.sidebar.success("✅ Base de datos actualizada")

# Header Principal
st.markdown(f"""
    <div class="main-header">
        <h2>📊 Control de Presupuesto y Gastos Fijos</h2>
        <p>Reginald Lee S.A. | Vista Ejecutiva — Usuario: <b>{st.session_state['user']}</b></p>
    </div>
""", unsafe_allow_html=True)

if df is not None:
    if not st.session_state['is_admin']:
        df_user = df[df['RESPONSABLE'].astype(str).str.upper() == st.session_state['user']]
    else:
        df_user = df.copy()

    # Filtros
    st.sidebar.subheader("🎯 Filtros Generales")
    meses_disponibles = sorted(df_user['MES_NOMBRE'].dropna().unique())
    locaciones_disponibles = sorted(df_user['LOCACION'].dropna().unique())
    grupos_disponibles = sorted(df_user['GRUPO DE CUENTAS'].dropna().unique())

    f_mes = st.sidebar.multiselect("Meses", meses_disponibles, default=meses_disponibles)
    f_loc = st.sidebar.multiselect("Locación / Planta", locaciones_disponibles, default=locaciones_disponibles)
    f_grupo = st.sidebar.multiselect("Grupo de Cuentas", grupos_disponibles, default=grupos_disponibles)

    if st.session_state['is_admin']:
        resps_disponibles = sorted(df_user['RESPONSABLE'].dropna().unique())
        f_resp = st.sidebar.multiselect("Responsable Sector", resps_disponibles, default=resps_disponibles)
    else:
        f_resp = [st.session_state['user']]

    # Dataset Filtrado
    df_f = df_user[
        (df_user['MES_NOMBRE'].isin(f_mes)) &
        (df_user['LOCACION'].isin(f_loc)) &
        (df_user['GRUPO DE CUENTAS'].isin(f_grupo)) &
        (df_user['RESPONSABLE'].astype(str).str.upper().isin(f_resp))
    ]

    presupuesto_df = df_f[df_f['TIPO2'] == 'PRESUPUESTO']
    gasto_df = df_f[df_f['TIPO2'] == 'GASTO']

    tot_presupuesto = presupuesto_df['SALDO'].sum()
    tot_gasto = abs(gasto_df['SALDO'].sum())
    desviacion = tot_gasto - tot_presupuesto
    pct_ejecucion = (tot_gasto / tot_presupuesto * 100) if tot_presupuesto > 0 else 0

    # KPI Cards
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(f"""
            <div class="custom-card">
                <div class="card-title">Presupuesto Asignado</div>
                <div class="card-value">{formato_moneda(tot_presupuesto)}</div>
            </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
            <div class="custom-card">
                <div class="card-title">Gasto Real Ejecutado</div>
                <div class="card-value">{formato_moneda(tot_gasto)}</div>
            </div>
        """, unsafe_allow_html=True)

    with k3:
        sub_color = "text-red" if desviacion > 0 else "text-green"
        st.markdown(f"""
            <div class="custom-card">
                <div class="card-title">Desviación Presupuestaria</div>
                <div class="card-value">{formato_moneda(desviacion)}</div>
                <div class="card-sub {sub_color}">Diferencia acumulada</div>
            </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
            <div class="custom-card">
                <div class="card-title">% Ejecución Presupuestaria</div>
                <div class="card-value">{pct_ejecucion:.1f}%</div>
                <div class="card-sub text-red" style="visibility: {'visible' if pct_ejecucion > 100 else 'hidden'};">Excedido de Presupuesto</div>
            </div>
        """, unsafe_allow_html=True)

    # Gráficos
    col_g1, col_g2, col_g3 = st.columns([1.5, 1.2, 1])

    with col_g1:
        st.markdown("### 📅 Presupuesto vs Real por Mes")
        p_mes = presupuesto_df.groupby('MES_NOMBRE')['SALDO'].sum().reset_index().rename(columns={'SALDO': 'Presupuesto'})
        g_mes = gasto_df.groupby('MES_NOMBRE')['SALDO'].apply(lambda x: abs(x.sum())).reset_index().rename(columns={'SALDO': 'Gasto Real'})
        comp_mes = pd.merge(p_mes, g_mes, on='MES_NOMBRE', how='outer').fillna(0)

        fig_mes = go.Figure()
        fig_mes.add_trace(go.Bar(x=comp_mes['MES_NOMBRE'], y=comp_mes['Presupuesto'], name='Presupuesto', marker_color='#9CA3AF'))
        fig_mes.add_trace(go.Bar(x=comp_mes['MES_NOMBRE'], y=comp_mes['Gasto Real'], name='Gasto Real', marker_color='#E61C24'))
        fig_mes.update_layout(
            paper_bgcolor='#111827', plot_bgcolor='#111827', font=dict(color='#FFFFFF'),
            xaxis=dict(gridcolor='#374151', tickfont=dict(color='#FFFFFF')),
            yaxis=dict(gridcolor='#374151', tickfont=dict(color='#FFFFFF')),
            barmode='group', height=300, margin=dict(l=15, r=15, t=15, b=15),
            legend=dict(orientation="h", y=1.15, font=dict(color='#FFFFFF'))
        )
        st.plotly_chart(fig_mes, use_container_width=True)

    with col_g2:
        st.markdown("### 📊 Gasto por Grupo de Cuentas")
        g_grupo = gasto_df.groupby('GRUPO DE CUENTAS')['SALDO'].apply(lambda x: abs(x.sum())).reset_index().sort_values(by='SALDO', ascending=True).tail(7)
        fig_grupo = px.bar(g_grupo, x='SALDO', y='GRUPO DE CUENTAS', orientation='h', color_discrete_sequence=['#E61C24'])
        fig_grupo.update_layout(
            paper_bgcolor='#111827', plot_bgcolor='#111827', font=dict(color='#FFFFFF'),
            xaxis=dict(gridcolor='#374151', tickfont=dict(color='#FFFFFF')),
            yaxis=dict(gridcolor='#374151', tickfont=dict(color='#FFFFFF')),
            height=300, margin=dict(l=15, r=15, t=15, b=15), xaxis_title="", yaxis_title=""
        )
        st.plotly_chart(fig_grupo, use_container_width=True)

    with col_g3:
        st.markdown("### 🎯 Nivel de Ejecución")
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = pct_ejecucion,
            number = {'suffix': "%", 'font': {'size': 28, 'color': '#FFFFFF', 'family': 'Arial'}},
            gauge = {
                'axis': {'range': [0, max(120, pct_ejecucion)], 'tickcolor': "#FFFFFF", 'tickfont': {'color': '#FFFFFF'}},
                'bar': {'color': "#E61C24" if pct_ejecucion > 100 else "#9CA3AF"},
                'steps': [
                    {'range': [0, 80], 'color': "#374151"},
                    {'range': [80, 100], 'color': "#4B5563"},
                    {'range': [100, max(120, pct_ejecucion)], 'color': "#991B1B"}
                ]
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor='#111827', plot_bgcolor='#111827', font=dict(color='#FFFFFF'),
            height=300, margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    # Segunda fila
    c_r2_1, c_r2_2 = st.columns([1, 1.5])

    with c_r2_1:
        st.markdown("### 🏢 Gastos por Locación")
        g_loc = gasto_df.groupby('LOCACION')['SALDO'].apply(lambda x: abs(x.sum())).reset_index()
        fig_loc = px.pie(
            g_loc, values='SALDO', names='LOCACION', hole=0.4,
            color_discrete_sequence=['#E61C24', '#6B7280', '#9CA3AF', '#D1D5DB', '#374151']
        )
        fig_loc.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(color='#FFFFFF'))
        fig_loc.update_layout(
            paper_bgcolor='#111827', plot_bgcolor='#111827', font=dict(color='#FFFFFF'),
            height=300, margin=dict(l=15, r=15, t=15, b=15), legend=dict(font=dict(color='#FFFFFF'))
        )
        st.plotly_chart(fig_loc, use_container_width=True)

    with c_r2_2:
        st.markdown("### ⚠️ Cuentas con Mayor Desviación")
        p_cta = presupuesto_df.groupby('DESC CTA CBLE')['SALDO'].sum().rename('Presupuesto')
        g_cta = gasto_df.groupby('DESC CTA CBLE')['SALDO'].apply(lambda x: abs(x.sum())).rename('Gasto Real')
        comp_cta = pd.concat([p_cta, g_cta], axis=1).fillna(0)
        comp_cta['Desviacion'] = comp_cta['Gasto Real'] - comp_cta['Presupuesto']
        top_desv = comp_cta.sort_values(by='Desviacion', ascending=False).head(5).reset_index()

        fig_desv = px.bar(
            top_desv, x='Desviacion', y='DESC CTA CBLE', orientation='h',
            color='Desviacion', color_continuous_scale=['#6B7280', '#E61C24']
        )
        fig_desv.update_layout(
            paper_bgcolor='#111827', plot_bgcolor='#111827', font=dict(color='#FFFFFF'),
            xaxis=dict(gridcolor='#374151', tickfont=dict(color='#FFFFFF')),
            yaxis=dict(gridcolor='#374151', tickfont=dict(color='#FFFFFF')),
            height=300, margin=dict(l=15, r=15, t=15, b=15), xaxis_title="Desviación en $", yaxis_title=""
        )
        st.plotly_chart(fig_desv, use_container_width=True)

    # Tabla Transaccional
    st.markdown("---")
    st.markdown("### 🔍 Consulta y Auditoría Transaccional de Gastos")

    df_auditoria = gasto_df.copy()

    cuentas_unicas = sorted(df_auditoria['DESC CTA CBLE'].dropna().unique())
    col_f1, col_f2 = st.columns([2, 1])
    
    with col_f1:
        f_cuentas_tabla = st.multiselect("🔎 Filtrar por Cuenta Contable:", cuentas_unicas, default=[])
    with col_f2:
        search_kw = st.text_input("💬 Buscar por Proveedor / N° Interno:", "")

    if f_cuentas_tabla:
        df_auditoria = df_auditoria[df_auditoria['DESC CTA CBLE'].isin(f_cuentas_tabla)]

    if search_kw:
        sk = search_kw.lower()
        mask = (
            df_auditoria['DES1'].astype(str).str.lower().str.contains(sk) |
            df_auditoria['INTERNO'].astype(str).str.lower().str.contains(sk) |
            df_auditoria['TEXTO INTERNO'].astype(str).str.lower().str.contains(sk)
        )
        df_auditoria = df_auditoria[mask]

    df_auditoria['MONTO_MOSTRAR'] = df_auditoria['SALDO'] * -1
    df_auditoria['MONTO_FORMATO'] = df_auditoria['MONTO_MOSTRAR'].apply(lambda v: formato_moneda(v, con_decimales=True))

    cols_tabla = [
        'FECHA', 'MES_NOMBRE', 'LOCACION', 'RESPONSABLE', 
        'GRUPO DE CUENTAS', 'DESC CTA CBLE', 'DES1', 'INTERNO', 'MONTO_FORMATO'
    ]

    df_render = df_auditoria[cols_tabla].rename(columns={
        'MES_NOMBRE': 'MES',
        'DESC CTA CBLE': 'CUENTA CONTABLE',
        'DES1': 'PROVEEDOR / ENTIDAD',
        'INTERNO': 'N° INTERNO',
        'MONTO_FORMATO': 'MONTO ($)'
    })

    st.dataframe(df_render, use_container_width=True, height=380)

    # Inspector
    st.markdown("#### 📌 Inspeccionar 'Texto Interno' de un Gasto Específico")
    
    if not df_auditoria.empty:
        opciones_inspeccion = df_auditoria.apply(
            lambda r: f"ID {r.name} | {r['FECHA']} | {r['DES1']} | {formato_moneda(r['MONTO_MOSTRAR'], con_decimales=True)} | {r['DESC CTA CBLE']}", axis=1
        ).tolist()
        
        selected_option = st.selectbox("Seleccione una transacción para desplegar su detalle completo:", opciones_inspeccion)
        
        if selected_option:
            selected_id = int(selected_option.split(" | ")[0].replace("ID ", ""))
            item_row = df_auditoria.loc[selected_id]
            
            st.markdown(f"""
                <div class="detail-popup">
                    <h5>📝 Texto Interno / Detalle Completo de la Compra</h5>
                    <p>"{item_row['TEXTO INTERNO']}"</p>
                    <hr>
                    <small><b>Proveedor:</b> {item_row['DES1']} | <b>Cuenta:</b> {item_row['DESC CTA CBLE']} | <b>N° Interno:</b> {item_row['INTERNO']} | <b>Comprobante:</b> {item_row['COMPROBANTE']}</small>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No hay registros disponibles para inspeccionar con los filtros actuales.")
