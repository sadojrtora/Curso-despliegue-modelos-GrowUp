from typing import Literal, Optional

from pydantic import BaseModel, Field


class LoanApplication(BaseModel):
    Gender: Optional[Literal["Male", "Female"]] = Field(
        default=None,
        description="Applicant gender.",
    )
    Married: Optional[Literal["Yes", "No"]] = Field(
        default=None,
        description="Whether the applicant is married.",
    )
    Dependents: Optional[Literal["0", "1", "2", "3+"]] = Field(
        default=None,
        description="Number of dependents; 3+ represents three or more.",
    )
    Education: Optional[Literal["Graduate", "Not Graduate"]] = Field(
        default=None,
        description="Applicant education level.",
    )
    Self_Employed: Optional[Literal["Yes", "No"]] = Field(
        default=None,
        description="Whether the applicant is self-employed.",
    )
    ApplicantIncome: Optional[float] = Field(
        default=None,
        ge=0,
        description="Applicant income.",
    )
    CoapplicantIncome: Optional[float] = Field(
        default=None,
        ge=0,
        description="Co-applicant income.",
    )
    LoanAmount: Optional[float] = Field(
        default=None,
        ge=0,
        description="Requested loan amount.",
    )
    Loan_Amount_Term: Optional[float] = Field(
        default=None,
        ge=0,
        description="Loan term in months.",
    )
    Credit_History: Optional[Literal[0, 1]] = Field(
        default=None,
        description="Credit history flag: 1 for positive history, 0 otherwise.",
    )
    Property_Area: Optional[Literal["Urban", "Rural", "Semiurban"]] = Field(
        default=None,
        description="Area where the property is located.",
    )


class LoanPrediction(BaseModel):
    loan_status: Literal["Y", "N"] = Field(
        description="Predicted loan decision: Y for approved, N for rejected.",
    )
    approval_probability: float = Field(
        ge=0,
        le=1,
        description="Predicted probability that the loan will be approved.",
    )