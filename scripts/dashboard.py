"""
Dashboard de Monitoramento - Books API
Dashboard Streamlit para visualização de métricas e logs da API.

Para executar:
    streamlit run scripts/dashboard.py
"""
import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Books API - Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

import os

# URL base da API
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")


def get_metrics():
    """Busca métricas da API."""
    try:
        response = requests.get(f"{API_BASE_URL}/metrics/", timeout=5)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        return None
    return None


def get_recent_requests(limit=50):
    """Busca requisições recentes."""
    try:
        response = requests.get(f"{API_BASE_URL}/metrics/requests?limit={limit}", timeout=5)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        return None
    return None


def get_health():
    """Verifica saúde da API."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        return None
    return None


# Sidebar
st.sidebar.title("📚 Books API")
st.sidebar.markdown("---")
auto_refresh = st.sidebar.checkbox("Auto-refresh (5s)", value=False)
if st.sidebar.button("🔄 Atualizar Agora"):
    st.rerun()

# Título principal
st.title("📊 Dashboard de Monitoramento")
st.markdown("Visualização em tempo real das métricas da Books API")

# Verifica se API está online
health = get_health()
if health:
    st.success(f"✅ API Online - Versão {health.get('version', 'N/A')}")
else:
    st.error("❌ API Offline - Verifique se a API está rodando em http://localhost:8000")
    st.stop()

# Busca métricas
metrics = get_metrics()

if metrics:
    # Métricas principais
    st.markdown("## 📈 Métricas Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total de Requisições",
            value=metrics["summary"]["total_requests"]
        )
    
    with col2:
        st.metric(
            label="Total de Erros",
            value=metrics["summary"]["total_errors"]
        )
    
    with col3:
        error_rate = metrics["summary"]["error_rate"]
        st.metric(
            label="Taxa de Erro",
            value=f"{error_rate}%",
            delta=None if error_rate == 0 else f"{error_rate}%",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            label="Uptime Desde",
            value=metrics["summary"]["uptime_since"][:10]
        )
    
    st.markdown("---")
    
    # Gráficos lado a lado
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Requisições por Endpoint")
        if metrics["by_endpoint"]:
            endpoint_data = []
            for endpoint, data in metrics["by_endpoint"].items():
                endpoint_data.append({
                    "Endpoint": endpoint,
                    "Requisições": data["requests"],
                    "Tempo Médio (ms)": data["avg_response_time_ms"],
                    "Erros": data["errors"]
                })
            df_endpoints = pd.DataFrame(endpoint_data)
            df_endpoints = df_endpoints.sort_values("Requisições", ascending=False)
            
            # Gráfico de barras
            st.bar_chart(df_endpoints.set_index("Endpoint")["Requisições"])
            
            # Tabela detalhada
            st.dataframe(df_endpoints, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum dado de endpoint disponível ainda.")
    
    with col2:
        st.markdown("### 📈 Distribuição por Status Code")
        if metrics["by_status_code"]:
            status_data = pd.DataFrame([
                {"Status": k, "Contagem": v}
                for k, v in metrics["by_status_code"].items()
            ])
            st.bar_chart(status_data.set_index("Status")["Contagem"])
        else:
            st.info("Nenhum dado de status code disponível ainda.")
        
        st.markdown("### 🔧 Requisições por Método HTTP")
        if metrics["by_method"]:
            method_data = pd.DataFrame([
                {"Método": k, "Contagem": v}
                for k, v in metrics["by_method"].items()
            ])
            st.bar_chart(method_data.set_index("Método")["Contagem"])
        else:
            st.info("Nenhum dado de método disponível ainda.")
    
    st.markdown("---")
    
    # Requisições recentes
    st.markdown("## 📋 Requisições Recentes")
    requests_data = get_recent_requests(limit=50)
    
    if requests_data:
        df_requests = pd.DataFrame(requests_data)
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.multiselect(
                "Filtrar por Status",
                options=df_requests["status_code"].unique().tolist(),
                default=[]
            )
        with col2:
            method_filter = st.multiselect(
                "Filtrar por Método",
                options=df_requests["method"].unique().tolist(),
                default=[]
            )
        with col3:
            endpoint_filter = st.text_input("Filtrar por Endpoint (contém)")
        
        # Aplica filtros
        if status_filter:
            df_requests = df_requests[df_requests["status_code"].isin(status_filter)]
        if method_filter:
            df_requests = df_requests[df_requests["method"].isin(method_filter)]
        if endpoint_filter:
            df_requests = df_requests[df_requests["endpoint"].str.contains(endpoint_filter, case=False)]
        
        # Formata e exibe
        columns_to_show = ["timestamp", "method", "endpoint", "status_code", "duration_ms", "client_ip"]
        df_display = df_requests[columns_to_show].rename(columns={
            "timestamp": "Timestamp",
            "method": "Método",
            "endpoint": "Endpoint",
            "status_code": "Status",
            "duration_ms": "Tempo (ms)",
            "client_ip": "IP"
        })
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma requisição registrada ainda.")

else:
    st.warning("Não foi possível carregar as métricas. Verifique a conexão com a API.")

# Footer
st.markdown("---")
st.markdown(
    f"*Última atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
)

# Auto-refresh
if auto_refresh:
    time.sleep(5)
    st.rerun()
