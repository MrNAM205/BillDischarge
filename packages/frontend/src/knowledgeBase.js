export const KNOWLEDGE_BASE = {
    // ... other knowledge base sections like FDCPA, FCRA, etc.

    Endorsements: {
        WithoutRecourse: {
            summary: 'Without Recourse (UCC § 3-415(b))',
            detail: 'This qualifier disclaims the endorser\'s liability to pay the instrument if it is dishonored. The person who takes the instrument cannot sue the endorser if the original maker fails to pay.'
        },
        ForDepositOnly: {
            summary: 'For Deposit Only (UCC § 3-206(c))',
            detail: 'This is a restrictive endorsement. It requires that the instrument be deposited into an account for the endorser. It prevents anyone else from cashing the check or depositing it into another account.'
        },
        UCC_1_308: {
            summary: 'Under Protest / Without Prejudice (UCC § 1-308)',
            detail: 'This indicates that you are performing an action (like cashing a check) but are explicitly reserving your rights to dispute the underlying obligation. You are not agreeing that the payment satisfies the full debt.'
        },
        AcceptedForValue: {
            summary: 'Accepted for Value (A4V)',
            detail: 'This is a controversial theory associated with sovereign citizen and redemption movements. It purports to "accept" a bill as value and use it to discharge a debt via a Treasury account. This is not recognized in mainstream commercial law and can carry legal risks.'
        }
    },

    UCC: {
        IsNegotiable: {
            label: "Is Negotiable Instrument",
            test: (text) => /negotiable/i.test(text),
            citation: "UCC § 3-104",
            remedyHint: "The instrument must be negotiable."
        },
        PromiseOrOrder: {
            label: "Contains a Promise or Order",
            test: (text) => /promise|order/i.test(text),
            citation: "UCC § 3-104(a)",
            remedyHint: "The instrument must contain an unconditional promise or order to pay."
        },
        UnconditionalPromiseOrOrder: {
            label: "Unconditional Promise or Order",
            test: (text) => !/subject to|governed by/i.test(text),
            citation: "UCC § 3-106",
            remedyHint: "The promise or order must be unconditional."
        },
        PayableOnDemandOrAtDefiniteTime: {
            label: "Payable on Demand or at Definite Time",
            test: (text) => /on demand|at sight|on presentation|\d{1,2}\/\d{1,2}\/\d{4}/i.test(text),
            citation: "UCC § 3-108",
            remedyHint: "The instrument must be payable on demand or at a definite time."
        },
        PayableToBearerOrToOrder: {
            label: "Payable to Bearer or to Order",
            test: (text) => /to bearer|to order|pay to the order of/i.test(text),
            citation: "UCC § 3-109",
            remedyHint: "The instrument must be payable to bearer or to order."
        },
        IdentificationOfPersonToWhomInstrumentIsPayable: {
            label: "Identification of Person to Whom Instrument is Payable",
            test: (text) => /pay to the order of [A-Z][a-z]+ [A-Z][a-z]+/i.test(text), // Basic test for a name
            citation: "UCC § 3-110",
            remedyHint: "The person to whom the instrument is payable must be identified with reasonable certainty."
        },
        PlaceOfPayment: {
            label: "Place of Payment",
            test: (text) => /\d{1,5}\s[A-Z][a-z]+\s(?:Street|Road|Avenue|Lane|Drive|Blvd|Place|Court|Cir|Ave|Rd|St|Dr|Ln|Blvd|Pl|Ct)\s*,\s*[A-Z][a-z]+\s*,\s*[A-Z]{2}\s*\d{5}/i.test(text), // Basic test for an address
            citation: "UCC § 3-111",
            remedyHint: "The instrument may indicate a place of payment."
        },
        Interest: {
            label: "Interest",
            test: (text) => /interest|\d{1,2}\.?\d{0,2}%/i.test(text),
            citation: "UCC § 3-112",
            remedyHint: "The instrument may provide for interest."
        },
        DateOfInstrument: {
            label: "Date of Instrument",
            test: (text) => /\d{1,2}\/\d{1,2}\/\d{4}/.test(text),
            citation: "UCC § 3-113",
            remedyHint: "The instrument may be antedated or postdated."
        },
        ContradictoryTermsOfInstrument: {
            label: "Contradictory Terms of Instrument",
            test: (text) => !/words prevail over numbers|handwritten terms prevail over printed terms|typewritten terms prevail over printed terms/i.test(text), // Basic test for contradictory terms
            citation: "UCC § 3-114",
            remedyHint: "If an instrument contains contradictory terms, words prevail over numbers, handwritten terms prevail over printed terms, and typewritten terms prevail over both."
        },
        IncompleteInstrument: {
            label: "Incomplete Instrument",
            test: (text) => !/___|blank|missing/i.test(text), // Basic test for incomplete instrument
            citation: "UCC § 3-115",
            remedyHint: "An incomplete instrument that is later completed in an unauthorized manner is enforceable as completed."
        },
        JointAndSeveralLiability: {
            label: "Joint and Several Liability",
            test: (text) => /(?:maker|acceptor|drawer|indorser)(?:\s*and\s*(?:maker|acceptor|drawer|indorser)){1,}/i.test(text), // Basic test for multiple signers
            citation: "UCC § 3-116",
            remedyHint: "Two or more persons who sign an instrument as maker, acceptor, or drawer, or indorser are jointly and severally liable."
        },
        OtherAgreementsAffectingInstrument: {
            label: "Other Agreements Affecting Instrument",
            test: (text) => /separate agreement|other agreement/i.test(text),
            citation: "UCC § 3-117",
            remedyHint: "The obligation of a party to an instrument may be modified, supplemented, or nullified by a separate agreement."
        },
        StatuteOfLimitations: {
            label: "Statute of Limitations",
            test: (text) => {
                const yearMatch = text.match(/\d{4}/);
                if (yearMatch) {
                    const year = parseInt(yearMatch[0]);
                    const currentYear = new Date().getFullYear();
                    return (currentYear - year) <= 6; // Basic test: within 6 years
                }
                return true; // No year found, assume within limits for now
            },
            citation: "UCC § 3-118",
            remedyHint: "An action to enforce the obligation of a party to a note payable at a definite time must be commenced within 6 years after the due date or dates stated in the note or, if a due date is not stated, within 6 years after the date of the instrument."
        },
        NoticeOfRightToDefendAction: {
            label: "Notice of Right to Defend Action",
            test: (text) => /notice of right to defend|vouch in/i.test(text),
            citation: "UCC § 3-119",
            remedyHint: "A person who is sued for an obligation for which another party is answerable over may give notice of the litigation to the other party."
        }
    },

    CouponRules: {
        UCCNegotiableCoupon: {
            label: "UCC Negotiable Coupon",
            test: (coupon) => {
                // This is a simplified check. A full check would involve all UCC Article 3 negotiability requirements.
                return coupon.type === 'Financial' &&
                       /unconditional promise|order/i.test(coupon.snippet) &&
                       /fixed amount/i.test(coupon.snippet) &&
                       /money/i.test(coupon.snippet) &&
                       (/to bearer|to order/i.test(coupon.snippet)) &&
                       (/on demand|definite time/i.test(coupon.snippet));
            },
            citation: "UCC Article 3",
            remedyHint: "This coupon may be a negotiable instrument under UCC Article 3. Ensure proper handling and endorsement."
        },
        USCFoodBenefitCoupon: {
            label: "USC/CFR Food/Benefit Coupon",
            test: (coupon) => {
                return coupon.type === 'Benefit' &&
                       (/food stamp|EBT|government benefit|assistance program/i.test(coupon.snippet));
            },
            citation: "42 U.S.C. § 1786(m)(10)(A), 7 CFR § 271.5",
            remedyHint: "This coupon may be subject to federal regulations regarding benefit transfers. Verify compliance with relevant laws (e.g., anti-counterfeiting, misuse)."
        },
        GeneralPromotionalCoupon: {
            label: "General Promotional Coupon",
            test: (coupon) => {
                return coupon.type === 'Promotional' ||
                       (/discount|promo code|rebate/i.test(coupon.snippet));
            },
            citation: "N/A",
            remedyHint: "This is a general promotional coupon. Review terms and conditions for validity and usage."
        }
    }
};