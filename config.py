import os
import base64
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
import mlflow
from dotenv import load_dotenv
from langfuse.openai import openai
from langchain_openai import ChatOpenAI

load_dotenv()

def setup_tracing():
    """
    Configure Langfuse and OpenTelemetry tracing with MLflow autologging for OpenAI.
    """
    # === Clés Langfuse ===
    langfuse_public_key = os.getenv("LF_PUBLIC_KEY")
    langfuse_secret_key = os.getenv("LF_SECRET_KEY")
    if not langfuse_public_key or not langfuse_secret_key:
        raise ValueError("Les clés Langfuse ne sont pas définies dans les variables d'environnement.")
    
    langfuse_auth = base64.b64encode(
        f"{langfuse_public_key}:{langfuse_secret_key}".encode()
    ).decode()

    # === Variables d'environnement OTLP ===
    os.environ["OTEL_EXPORTER_OTLP_TRACES_ENDPOINT"] = "https://cloud.langfuse.com/api/public/otel/v1/traces"
    os.environ["OTEL_EXPORTER_OTLP_TRACES_HEADERS"] = f"Authorization=Basic {langfuse_auth}"
    os.environ["OTEL_EXPORTER_OTLP_TRACES_PROTOCOL"] = "http/protobuf"

    # === Crée un TracerProvider global (unique) ===
    trace_provider = TracerProvider()
    trace_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter()))
    trace.set_tracer_provider(trace_provider)

    # === Crée un tracer ===
    tracer = trace.get_tracer(__name__)
    print("Tracer configuré:", tracer)

    # === Active l'autolog MLflow pour OpenAI ===
    mlflow.openai.autolog()

    print(tracer)
    return tracer


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
