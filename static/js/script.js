document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       SMOOTH SCROLLING
    ===================================================== */

    window.scrollToAnalyze = function () {

        const section = document.querySelector(".analyze-section");

        if (section) {
            section.scrollIntoView({
                behavior: "smooth"
            });
        }
    };


    window.scrollToHowItWorks = function () {

        const section = document.querySelector(".how-section");

        if (section) {
            section.scrollIntoView({
                behavior: "smooth"
            });
        }
    };


    /* =====================================================
       CREATE NLP SECTION
    ===================================================== */

    const analyzeSection = document.querySelector(".analyze-section");

    if (analyzeSection) {

        const nlpBox = document.createElement("div");

        nlpBox.id = "nlpAnalysisBox";

        nlpBox.innerHTML = `

            <div style="
                max-width:950px;
                margin:0 auto 30px;
                background:white;
                border:1px solid #dbeafe;
                border-radius:18px;
                padding:30px;
                box-shadow:0 12px 35px rgba(15,23,42,0.05);
            ">

                <div style="
                    display:flex;
                    align-items:center;
                    gap:10px;
                    margin-bottom:10px;
                ">

                    <span style="
                        font-size:25px;
                    ">
                        🤖
                    </span>

                    <h2 style="
                        margin:0;
                        color:#111827;
                        font-size:24px;
                    ">
                        AI Profile Analysis
                    </h2>

                </div>


                <p style="
                    color:#64748b;
                    margin-bottom:20px;
                    font-size:14px;
                ">
                    Describe yourself naturally and
                    WelfareSense AI will extract your
                    profile information automatically.
                </p>


                <textarea
                    id="nlpInput"
                    placeholder="Example: I am a 20 year old graduate student from Telangana. My annual family income is 2 lakh rupees and I am looking for government jobs."
                    style="
                        width:100%;
                        min-height:130px;
                        padding:15px;
                        border:1px solid #d9e0e8;
                        border-radius:10px;
                        resize:vertical;
                        font-family:Arial, sans-serif;
                        font-size:14px;
                        outline:none;
                        box-sizing:border-box;
                    "
                ></textarea>


                <button
                    id="nlpAnalyzeButton"
                    style="
                        margin-top:15px;
                        width:100%;
                        padding:14px;
                        border:none;
                        border-radius:9px;
                        background:#2563eb;
                        color:white;
                        font-size:15px;
                        font-weight:600;
                        cursor:pointer;
                    "
                >
                    🤖 Analyze with AI
                </button>


                <div
                    id="nlpStatus"
                    style="
                        margin-top:15px;
                        display:none;
                        padding:14px;
                        border-radius:9px;
                        font-size:13px;
                    "
                ></div>

            </div>

        `;


        /*
         * Insert NLP section at the top
         * of the Analyze section.
         */

        analyzeSection.insertBefore(
            nlpBox,
            analyzeSection.firstChild
        );


        /* =================================================
           NLP BUTTON
        ================================================= */

        const nlpButton =
            document.getElementById("nlpAnalyzeButton");

        const nlpInput =
            document.getElementById("nlpInput");

        const nlpStatus =
            document.getElementById("nlpStatus");


        if (nlpButton && nlpInput && nlpStatus) {

            nlpButton.addEventListener(
                "click",
                async function () {

                    const text =
                        nlpInput.value.trim();


                    if (!text) {

                        nlpStatus.style.display = "block";

                        nlpStatus.style.background =
                            "#fee2e2";

                        nlpStatus.style.color =
                            "#991b1b";

                        nlpStatus.textContent =
                            "Please describe your profile first.";

                        return;
                    }


                    /* -----------------------------------------
                       BUTTON LOADING STATE
                    ----------------------------------------- */

                    nlpButton.disabled = true;

                    nlpButton.textContent =
                        "🤖 Analyzing your profile...";


                    nlpStatus.style.display = "block";

                    nlpStatus.style.background =
                        "#eff6ff";

                    nlpStatus.style.color =
                        "#1e40af";

                    nlpStatus.textContent =
                        "Extracting your profile information...";


                    try {

                        const response =
                            await fetch(
                                "/analyze-text",
                                {
                                    method: "POST",

                                    headers: {
                                        "Content-Type":
                                            "application/json"
                                    },

                                    body:
                                        JSON.stringify({
                                            text: text
                                        })
                                }
                            );


                        const result =
                            await response.json();


                        if (!response.ok) {

                            throw new Error(
                                result.message ||
                                "Unable to analyze the profile."
                            );
                        }


                        /* -------------------------------------
                           SHOW EXTRACTED INFORMATION
                        ------------------------------------- */

                        const profile =
    result.user ||
    result.extracted_profile ||
    result.extractedProfile ||
    result.profile ||
    {};
console.log("Profile being saved:", result.user);
console.log("Results count:", result.results?.length);
console.log("NLP API response:", result);
console.log("Profile received:", profile);


                        nlpStatus.style.background =
                            "#f0fdf4";

                        nlpStatus.style.color =
                            "#166534";


                        nlpStatus.innerHTML = `

                            <strong>
                                ✅ Profile extracted successfully
                            </strong>

                            <br><br>

                            <strong>Name:</strong>
                            ${profile.name || "Not detected"}

                            &nbsp; | &nbsp;

                            <strong>Age:</strong>
                            ${profile.age || "Not detected"}

                            &nbsp; | &nbsp;

                            <strong>Income:</strong>
                            ${
                                profile.income
                                    ? "₹" +
                                      Number(profile.income)
                                          .toLocaleString("en-IN")
                                    : "Not detected"
                            }

                            <br>

                            <strong>Occupation:</strong>
                            ${profile.occupation || "Not detected"}

                            &nbsp; | &nbsp;

                            <strong>Education:</strong>
                            ${profile.education || "Not detected"}

                            <br>

                            <strong>State:</strong>
                            ${profile.state || "Not detected"}

                            &nbsp; | &nbsp;

                            <strong>Category:</strong>
                            ${profile.category || "Not detected"}

                            <br>

                            <strong>Area:</strong>
                            ${profile.area || "Not detected"}

                            &nbsp; | &nbsp;

                            <strong>Service:</strong>
                            ${profile.service_type || "Not detected"}

                        `;


                        /*
                         * Store result in BOTH storages.
                         * This prevents the results page
                         * from showing "Loading..." after
                         * NLP analysis.
                         */

                        const resultString =
                            JSON.stringify(result);

                        sessionStorage.setItem(
                            "welfareSenseResult",
                            resultString
                        );

                        sessionStorage.setItem("welfareSenseResult", JSON.stringify(result));


                        /*
                         * Small delay so the user can see
                         * the extracted profile.
                         */

                        setTimeout(
                            function () {

                                window.location.href =
                                    "/results";

                            },
                            1000
                        );

                    }


                    catch (error) {

                        console.error(error);


                        nlpStatus.style.background =
                            "#fee2e2";

                        nlpStatus.style.color =
                            "#991b1b";

                        nlpStatus.textContent =
                            "❌ " + error.message;


                        nlpButton.disabled = false;

                        nlpButton.textContent =
                            "🤖 Analyze with AI";

                    }

                }
            );

        }

    }


    /* =====================================================
       NORMAL FORM ANALYSIS
    ===================================================== */

    const form =
        document.querySelector("form");


    if (form) {

        form.addEventListener(
            "submit",
            async function (event) {

                event.preventDefault();


                const formData =
                    new FormData(form);


                const incomeRange =
                    formData.get("income");


                /*
                 * Convert income range into
                 * representative numeric income.
                 */

                const incomeMap = {

                    "below1":
                        50000,

                    "1to3":
                        200000,

                    "3to5":
                        400000,

                    "5to8":
                        650000,

                    "above8":
                        1000000

                };


                const data = {

                    name:
                        formData.get("name") || "",

                    age:
                        Number(
                            formData.get("age") || 0
                        ),

                    income:
                        incomeMap[incomeRange] || 0,

                    occupation:
                        formData.get("occupation") || "",

                    education:
                        formData.get("education") || "",

                    state:
                        formData.get("state") || "",

                    category:
                        formData.get("category") || "",

                    area:
                        formData.get("area") || "",

                    service_type:
                        formData.get("service_type") || ""

                };


                const analyzeButton =
                    form.querySelector(
                        "button[type='submit']"
                    );


                if (analyzeButton) {

                    analyzeButton.disabled = true;

                    analyzeButton.textContent =
                        "Analyzing...";

                }


                try {

                    const response =
                        await fetch(
                            "/analyze",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body:
                                    JSON.stringify(data)

                            }
                        );


                    const result =
                        await response.json();


                    if (!response.ok) {

                        throw new Error(
                            result.message ||
                            "Analysis failed."
                        );

                    }


                    const resultString =
                        JSON.stringify(result);


                    sessionStorage.setItem(
                        "welfareSenseResult",
                        resultString
                    );


                    localStorage.setItem(
                        "welfareSenseResult",
                        resultString
                    );


                    window.location.href =
                        "/results";

                }


                catch (error) {

                    console.error(error);

                    alert(error.message);


                    if (analyzeButton) {

                        analyzeButton.disabled = false;

                        analyzeButton.textContent =
                            "Analyze Eligibility";

                    }

                }

            }
        );

    }

});