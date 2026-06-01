# Author Verification Evidence Summary

This file summarizes what the supplied manuscript package supports for the seven author-only values that must be verified before removing `AUTHOR_VERIFY` markers from the revised manuscript.

| Verification item | Evidence found in supplied files | Still missing |
|---|---|---|
| AV1 inter-rater agreement / duplicate handling | Original manuscript states that three practicing dentists with more than 5 years of clinical experience independently annotated labels and that a fourth senior chief physician adjudicated disagreements. | Exact Fleiss' kappa value; duplicate/near-duplicate image count; source annotation sheet. |
| AV2 final statistics | Original manuscript reports point estimates, including 92.6% classification accuracy, 89.7% faithfulness, 98.2% action accuracy, 2.26 s latency, and broad user-study improvements. | Final bootstrap CIs, p-values, effect sizes, correction method/output. |
| AV3 latency logs | Original manuscript confirms dual NVIDIA GeForce RTX 4090 GPUs, 128 GB DDR5 RAM, AMD Ryzen 9 7950X, Ubuntu 22.04, PyTorch 2.1.0, and X-ODA average end-to-end latency of 2.26 s. | Per-baseline single-image latency logs for all nine models; warm-up rule; batch size. |
| AV4 dentist demographics / questionnaire | Original manuscript states that 12 practicing dentists participated, including 6 senior attending physicians and 6 junior resident physicians, and each evaluated 100 independent oral cases. | Age, gender, specialty distribution, exact years of experience, IRB-approved questionnaire wording. |
| AV5 Fig. 9 values | Original manuscript reports approximate outcomes: about 70% diagnostic-time reduction, early lesion detection above 91%, and trust score above 6.5/7. | Final manual/X-ODA values and confidence intervals for all Fig. 9 panels. |
| AV6 funding | No explicit funding or grant statement was found in the supplied manuscript, title page, cover letter, author agreement, or response files. No-conflict statements are not funding confirmation. | Author confirmation of no funding, or funder/grant information. |
| AV7 ethics / consent | Original manuscript states that clinical data were strictly de-identified, that data usage protocols were approved by ethics committees of collaborating institutions, and that the study complied with the Declaration of Helsinki. | Exact ethics committee name, approval number/date, and informed-consent or waiver wording. |

The public template intentionally keeps all seven `author_confirmed_value` and `source_record_checked` fields as `TODO`; private ethics identifiers or sensitive source records should only be added if the authors intentionally approve public disclosure.
