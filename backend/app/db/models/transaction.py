import uuid
from sqlalchemy import Column, Float, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
from sqlalchemy.dialects.postgresql import JSONB




class Transaction(Base):
    __tablename__ = "transactions"


    # CORE IDENTIFIERS
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # IEEE primary key (string-safe)
    TransactionID = Column(String, unique=True, index=True)

    ingested_at = Column(TIMESTAMP)


    # TRANSACTION CORE
    TransactionAmt = Column(Float, nullable=False)
    ProductCD = Column(String, nullable=True)


    # CARD / ADDRESS (ENTITY PROXIES)
    card1 = Column(Float, nullable=True)
    card2 = Column(Float, nullable=True)
    card3 = Column(Float, nullable=True)
    card4 = Column(String, nullable=True)
    card5 = Column(Float, nullable=True)
    card6 = Column(String, nullable=True)

    addr1 = Column(Float, nullable=True)
    addr2 = Column(Float, nullable=True)


    # COUNT FEATURES
    C1 = Column(Float, nullable=True)
    C2 = Column(Float, nullable=True)
    C3 = Column(Float, nullable=True)
    C4 = Column(Float, nullable=True)
    C5 = Column(Float, nullable=True)
    C6 = Column(Float, nullable=True)
    C7 = Column(Float, nullable=True)
    C8 = Column(Float, nullable=True)
    C9 = Column(Float, nullable=True)
    C10 = Column(Float, nullable=True)
    C11 = Column(Float, nullable=True)
    C12 = Column(Float, nullable=True)
    C13 = Column(Float, nullable=True)
    C14 = Column(Float, nullable=True)


    # TIME DELTA FEATURES
    D1 = Column(Float, nullable=True)
    D2 = Column(Float, nullable=True)
    D3 = Column(Float, nullable=True)
    D4 = Column(Float, nullable=True)
    D5 = Column(Float, nullable=True)
    D6 = Column(Float, nullable=True)
    D7 = Column(Float, nullable=True)
    D8 = Column(Float, nullable=True)
    D9 = Column(Float, nullable=True)
    D10 = Column(Float, nullable=True)
    D11 = Column(Float, nullable=True)
    D12 = Column(Float, nullable=True)
    D13 = Column(Float, nullable=True)
    D14 = Column(Float, nullable=True)
    D15 = Column(Float, nullable=True)


    # IDENTITY FEATURES
    DeviceType = Column(String, nullable=True)
    DeviceInfo = Column(String, nullable=True)

    id_01 = Column(Float, nullable=True)
    id_02 = Column(Float, nullable=True)
    id_03 = Column(Float, nullable=True)
    id_04 = Column(Float, nullable=True)
    id_05 = Column(Float, nullable=True)
    id_06 = Column(Float, nullable=True)
    id_07 = Column(Float, nullable=True)
    id_08 = Column(Float, nullable=True)
    id_09 = Column(Float, nullable=True)
    id_10 = Column(Float, nullable=True)
    id_11 = Column(Float, nullable=True)

    id_12 = Column(String, nullable=True)
    id_13 = Column(Float, nullable=True)
    id_14 = Column(Float, nullable=True)
    id_15 = Column(String, nullable=True)
    id_16 = Column(String, nullable=True)

    # THESE MUST BE FLOAT (NaN-heavy in IEEE)
    id_17 = Column(Float, nullable=True)
    id_18 = Column(Float, nullable=True)
    id_19 = Column(Float, nullable=True)
    id_20 = Column(Float, nullable=True)
    id_21 = Column(Float, nullable=True)
    id_22 = Column(Float, nullable=True)

    id_23 = Column(String, nullable=True)
    id_24 = Column(Float, nullable=True)
    id_25 = Column(Float, nullable=True)
    id_26 = Column(Float, nullable=True)
    id_27 = Column(String, nullable=True)
    id_28 = Column(String, nullable=True)
    id_29 = Column(String, nullable=True)
    id_30 = Column(String, nullable=True)
    id_31 = Column(String, nullable=True)
    id_32 = Column(Float, nullable=True)
    id_33 = Column(String, nullable=True)
    id_34 = Column(String, nullable=True)
    id_35 = Column(String, nullable=True)
    id_36 = Column(String, nullable=True)
    id_37 = Column(String, nullable=True)
    id_38 = Column(String, nullable=True)


    # MODEL OUTPUTS
    fraud_prob = Column(Float)
    anomaly_score = Column(Float)
    decision = Column(String)
    severity = Column(String)
    decision_reasons = Column(JSONB, nullable=True)
    shap_values = Column(JSONB, nullable=True)


    # HUMAN-IN-THE-LOOP
    analyst_decision = Column(String, nullable=True)
    analyst_reason = Column(String, nullable=True)
