// ==========================================================================
// Configuration
// ==========================================================================
const API_URL = "http://127.0.0.1:8000/Predict";

// ==========================================================================
// Element references
// ==========================================================================
const form = document.getElementById("predictForm");
const submitBtn = document.getElementById("submitBtn");
const resetBtn = document.getElementById("resetBtn");
const loadingIndicator = document.getElementById("loadingIndicator");
const apiError = document.getElementById("apiError");
const apiErrorText = document.getElementById("apiErrorText");
const resultCard = document.getElementById("resultCard");
const scoreValueEl = document.getElementById("scoreValue");
const gaugeFillEl = document.getElementById("gaugeFill");
const interpretationText = document.getElementById("interpretationText");

const fields = {
  age: document.getElementById("age"),
  gender: document.getElementById("gender"),
  country: document.getElementById("country"),
  academicLevel: document.getElementById("academicLevel"),
  platform: document.getElementById("platform"),
  purpose: document.getElementById("purpose"),
  dailyUsage: document.getElementById("dailyUsage"),
  dailyUnlocks: document.getElementById("dailyUnlocks"),
  studyHours: document.getElementById("studyHours"),
  activityHours: document.getElementById("activityHours"),
  sleepHours: document.getElementById("sleepHours"),
  stressLevel: document.getElementById("stressLevel"),
};

// Validation rules: min/max only apply to numeric fields.
const validationRules = {
  age: { min: 1, max: 150, label: "Age" },
  gender: { required: true, label: "Gender" },
  country: { required: true, label: "Country" },
  academicLevel: { required: true, label: "Academic level" },
  platform: { required: true, label: "Most used platform" },
  purpose: { required: true, label: "Purpose of use" },
  dailyUsage: { min: 1, max: 24, label: "Average daily usage hours" },
  dailyUnlocks: { min: 1, max: 500, label: "Daily unlocks" },
  studyHours: { min: 1, max: 24, label: "Study hours" },
  activityHours: { min: 1, max: 24, label: "Physical activity hours" },
  sleepHours: { min: 1, max: 24, label: "Sleep hours per night" },
  stressLevel: { required: true, label: "Stress level" },
};

let isSubmitting = false;

// ==========================================================================
// Validation helpers
// ==========================================================================
function getErrorEl(fieldEl) {
  const id = fieldEl.getAttribute("aria-describedby");
  return id ? document.getElementById(id) : null;
}

function setFieldError(fieldEl, message) {
  fieldEl.classList.add("invalid");
  const errorEl = getErrorEl(fieldEl);
  if (errorEl) errorEl.textContent = message;
}

function clearFieldError(fieldEl) {
  fieldEl.classList.remove("invalid");
  const errorEl = getErrorEl(fieldEl);
  if (errorEl) errorEl.textContent = "";
}

function validateField(key) {
  const fieldEl = fields[key];
  const rule = validationRules[key];
  const rawValue = fieldEl.value.trim();

  if (rawValue === "") {
    setFieldError(fieldEl, `${rule.label} is required.`);
    return false;
  }

  if (typeof rule.min === "number" || typeof rule.max === "number") {
    const numericValue = Number(rawValue);
    if (Number.isNaN(numericValue)) {
      setFieldError(fieldEl, `${rule.label} must be a number.`);
      return false;
    }
    if (numericValue < rule.min || numericValue > rule.max) {
      setFieldError(fieldEl, `${rule.label} must be between ${rule.min} and ${rule.max}.`);
      return false;
    }
  }

  clearFieldError(fieldEl);
  return true;
}

function validateAllFields() {
  let firstInvalidEl = null;
  let allValid = true;

  Object.keys(fields).forEach((key) => {
    const isValid = validateField(key);
    if (!isValid) {
      allValid = false;
      if (!firstInvalidEl) firstInvalidEl = fields[key];
    }
  });

  if (firstInvalidEl) firstInvalidEl.focus();
  return allValid;
}

// Remove the error state live as the user corrects a field.
Object.keys(fields).forEach((key) => {
  const fieldEl = fields[key];
  fieldEl.addEventListener("input", () => {
    if (fieldEl.classList.contains("invalid")) {
      validateField(key);
    }
  });
  fieldEl.addEventListener("change", () => {
    if (fieldEl.classList.contains("invalid")) {
      validateField(key);
    }
  });
});

// ==========================================================================
// Payload construction
// ==========================================================================
function buildPayload() {
  return {
    Age: Number(fields.age.value),
    Gender: fields.gender.value,
    Country: fields.country.value,
    Academic_Level: fields.academicLevel.value,
    Most_Used_Platform: fields.platform.value,
    Purpose_Of_Use: fields.purpose.value,
    Avg_Daily_Usage_Hours: Number(fields.dailyUsage.value),
    Daily_Unlocks: Number(fields.dailyUnlocks.value),
    Study_Hours: Number(fields.studyHours.value),
    Physical_Activity_Hours: Number(fields.activityHours.value),
    Sleep_Hours_Per_Night: Number(fields.sleepHours.value),
    Stress_Level: fields.stressLevel.value,
  };
}

// ==========================================================================
// UI state helpers
// ==========================================================================
function showLoading() {
  loadingIndicator.hidden = false;
  form.setAttribute("aria-busy", "true");
  submitBtn.disabled = true;
  submitBtn.querySelector(".btn-label").innerHTML =
    '<i class="fa-solid fa-spinner fa-spin" aria-hidden="true"></i> Analyzing...';
}

function hideLoading() {
  loadingIndicator.hidden = true;
  form.setAttribute("aria-busy", "false");
  submitBtn.disabled = false;
  submitBtn.querySelector(".btn-label").innerHTML =
    '<i class="fa-solid fa-chart-simple" aria-hidden="true"></i> Predict my score';
}

function showApiError(message) {
  apiErrorText.textContent = message;
  apiError.hidden = false;
}

function hideApiError() {
  apiError.hidden = true;
  apiErrorText.textContent = "";
}

// ==========================================================================
// Result rendering
// ==========================================================================
// NOTE: The scoring scale below assumes a 0–10 range for the gauge fill and
// the interpretation thresholds. Adjust GAUGE_MAX and the threshold values
// in getInterpretation() once the true range of the trained model's
// Health_score output is confirmed against the training dataset.
const GAUGE_MAX = 10;
const GAUGE_CIRCUMFERENCE = 2 * Math.PI * 80; // matches r="80" in the SVG

function getInterpretation(score) {
  // ---- Adjust these thresholds to match the model's real score distribution ----
  if (score < GAUGE_MAX * 0.4) {
    return "Your responses indicate that additional attention to wellbeing habits may be helpful.";
  }
  if (score < GAUGE_MAX * 0.7) {
    return "Your responses indicate a moderate wellbeing pattern.";
  }
  return "Your responses indicate a comparatively positive wellbeing pattern.";
}

function renderResult(score) {
  const clampedScore = Math.max(0, Math.min(GAUGE_MAX, score));
  const fraction = clampedScore / GAUGE_MAX;
  const offset = GAUGE_CIRCUMFERENCE * (1 - fraction);

  scoreValueEl.textContent = score.toFixed(2);
  gaugeFillEl.style.strokeDashoffset = String(offset);
  interpretationText.textContent = getInterpretation(clampedScore);

  resultCard.hidden = false;
  resultCard.scrollIntoView({ behavior: "smooth", block: "start" });
}

// ==========================================================================
// Form submission
// ==========================================================================
form.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (isSubmitting) return;

  hideApiError();

  if (!validateAllFields()) {
    return;
  }

  isSubmitting = true;
  showLoading();

  try {
    const payload = buildPayload();

    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      if (response.status === 400) {
        const err = await response.json();
        throw new Error(err.detail)}
      if (response.status === 422) {
        throw new Error("The server rejected some of the submitted values. Please check your entries and try again.");
      }
      if (response.status >= 500) {
        throw new Error("The prediction server ran into a problem. Please try again in a moment.");
      }
      throw new Error(`The server responded with an unexpected status (${response.status}).`);
    }

    let data;
    try {
      data = await response.json();
    } catch (parseError) {
      console.error("Failed to parse API response as JSON:", parseError);
      throw new Error("The server sent back a response that could not be understood.");
    }

    if (!data || typeof data.Health_Score !== "number") {
      console.error("Unexpected API response shape:", data);
      throw new Error("The server response did not include a valid score.");
    }

    renderResult(data.Health_Score);
  } catch (error) {
    console.error("Prediction request failed:", error);

    let friendlyMessage;
    if (error instanceof TypeError) {
      // fetch() throws a TypeError for network failures and CORS issues.
      friendlyMessage =
        "Could not reach the prediction server. Make sure the FastAPI backend is running at " +
        "http://127.0.0.1:8000 and that CORS is enabled for this page.";
    } else {
      friendlyMessage = error.message || "Something went wrong while getting your prediction.";
    }

    showApiError(friendlyMessage);
  } finally {
    hideLoading();
    isSubmitting = false;
  }
});

// ==========================================================================
// Reset handling
// ==========================================================================
resetBtn.addEventListener("click", () => {
  // Native reset clears field values; the following clears our own UI state.
  window.setTimeout(() => {
    Object.keys(fields).forEach((key) => clearFieldError(fields[key]));
    hideApiError();
    resultCard.hidden = true;
    scoreValueEl.textContent = "0.00";
    gaugeFillEl.style.strokeDashoffset = String(GAUGE_CIRCUMFERENCE);
    interpretationText.textContent = "";
  }, 0);
});