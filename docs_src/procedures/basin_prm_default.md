---
kind: procedure
symbol: basin_prm_default
title: basin_prm_default
status: filled
source_hash: eb31556688e569d5
version_label: SWAT+ 62.0.0
uses:
  basin_module: '`basin_module` defines the shared basin parameter object `bsn_prm` that this
    routine populates. The routine exists to repair or initialize many basin-scale parameters
    in that module before the rest of the basin and routing code uses them.'
  hru_module: '`hru_module` provides the shared `uptake` structure whose normalization fields
    are set here. Those values matter because HRU uptake calculations use the normalized water,
    nitrogen, and phosphorus distribution settings later in the simulation.'
  utils: '`utils` matters because this routine calls `exp_w` when computing `uptake%p_norm`;
    the wrapped exponential avoids underflow for the phosphorus uptake normalization when
    `-bsn_prm%p_updis` is very negative.'
---

<!-- facts:header -->

Initializes basin-wide default parameters and derived uptake normalization values for the SWAT+ basin setup.

## Bottom Line

`basin_prm_default` fills in missing basin parameter defaults after basin parameters are read, then derives a few normalized uptake settings and the maximum output lag days. It is part of basin initialization, so later basin, HRU, and routing calculations start from a complete parameter set.

It guards against near-zero or unset values for many `bsn_prm` fields, converts `petco_pmpt` from a percentage-style input to a fraction, and hardwires the water uptake distribution before computing `water_norm`, `n_norm`, and `p_norm`. Those derived values feed later HRU uptake behavior and output storage limits.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`proc_bsn` calls `basin_prm_default` after `basin_read_prm` has loaded basin inputs and before later basin setup routines such as `basin_print_codes_read`, `co2_read`, `carbon_bsn_read`, and `carbon_layers_read`. Its results establish default basin parameters and derived uptake scalars that downstream basin, HRU, and output-lag behavior depends on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check each basin parameter and assign a default when the value is effectively unset. | The routine scans the shared `bsn_prm` fields one by one. For each parameter, if the current value is below the small threshold used as a missing-value test, it assigns the documented default such as `evlai = 3.0`, `surlag = 4.0`, `n_updis = 20.0`, `rsd_covco = 0.75`, or `co2 = 400.0`. |
| 2. Mark the start of derived parameter setup. | The comment announces that the following assignments are not plain defaults but additional derived parameters for later model use. |
| 3. Hardwire the HRU water uptake distribution. | The routine sets `uptake%water_dis` to 10.0 and explicitly notes that users are not allowed to modify it. |
| 4. Compute the water uptake normalization factor. | It evaluates `uptake%water_norm = 1. - exp(-uptake%water_dis)`, turning the fixed water distribution into a normalized coefficient. |
| 5. Compute the nitrogen uptake normalization factor from basin input. | It evaluates `uptake%n_norm = 1. - exp(-bsn_prm%n_updis)`, using the basin nitrogen uptake distribution parameter that may have just been defaulted. |
| 6. Compute the phosphorus uptake normalization factor with overflow-safe exponential handling. | It evaluates `uptake%p_norm = 1. - exp_w(-bsn_prm%p_updis)`, using the wrapped exponential from `utils` to avoid numerical underflow for the phosphorus uptake distribution parameter. |
| 7. Set the maximum output lag days. | The routine sets `bsn_prm%day_lag_mx = 2`, establishing the maximum number of days to lag HRU, RU, and channel output storage. |
| 8. Return to the caller. | The subroutine exits after finishing basin default initialization and derived parameter setup. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%evlai, bsn_prm%ffcb, bsn_prm%surlag, bsn_prm%adj_pkr, bsn_prm%prf, bsn_prm%cmn, bsn_prm%n_updis, bsn_prm%p_updis, bsn_prm%nperco, bsn_prm%pperco, bsn_prm%phoskd, bsn_prm%psp, bsn_prm%rsdco, bsn_prm%percop, bsn_prm%msk_co1, bsn_prm%msk_co2, bsn_prm%msk_x, bsn_prm%nperco_lchtile, bsn_prm%evrch, bsn_prm%cdn, bsn_prm%sdnco, bsn_prm%bact_swf, bsn_prm%tb_adj, bsn_prm%cn_froz, bsn_prm%nfixmx, bsn_prm%decr_min, bsn_prm%rsd_covco, bsn_prm%urb_init_abst, bsn_prm%petco_pmpt, bsn_prm%uhalpha, bsn_prm%eros_spl, bsn_prm%rill_mult, bsn_prm%eros_expo, bsn_prm%c_factor, bsn_prm%ch_d50, bsn_prm%co2, bsn_prm%day_lag_mx` |
| [sym:hru_module] | `uptake` | `uptake%water_dis, uptake%water_norm, uptake%n_norm, uptake%p_norm` |
| [sym:utils] | `utils::exp_w` | `exp_w` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `bsn_prm%petco_pmpt` | `if (bsn_prm%petco_pmpt < 0.5 .and. bsn_prm%petco_pmpt > 0.)` followed by unconditional conversion on line 44 | `petco_pmpt` is coerced to zero when it is a small positive fraction, then converted from a percent-style input to a fraction with `(100. + bsn_prm%petco_pmpt) / 100.`. This prepares the basin PET adjustment value for later use in water balance and related calculations. |
| `uptake%water_dis` | Always set during the derived-parameter block | `uptake%water_dis` is hardwired to 10.0 so the water uptake distribution is fixed and not user-tunable in this routine. |
| `uptake%water_norm` | After `uptake%water_dis` is assigned | `uptake%water_norm` is derived from the fixed water distribution as `1. - exp(-uptake%water_dis)`, giving the normalized coefficient used by HRU water uptake logic. |
| `uptake%n_norm` | After basin nitrogen distribution defaults are ensured | `uptake%n_norm` is derived from `bsn_prm%n_updis` as `1. - exp(-bsn_prm%n_updis)`, normalizing the basin nitrogen uptake distribution for later HRU uptake calculations. |
| `uptake%p_norm` | After basin phosphorus distribution defaults are ensured | `uptake%p_norm` is derived from `bsn_prm%p_updis` as `1. - exp_w(-bsn_prm%p_updis)`, using the safe exponential wrapper to avoid underflow when phosphorus uptake distribution values are large. |
| `bsn_prm%day_lag_mx` | Always set near the end of the subroutine | `bsn_prm%day_lag_mx` is set to 2 so the model has a small, fixed maximum lag window for HRU, RU, and channel outputs. |

## File I/O

<!-- facts:io -->


## Lineage

`basin_prm_default` was added in df07e3f with the full basin default-initialization logic. c7c8e22 only carried the file forward from Bitbucket without changing the routine body. 3bb22ed changed the default `rsd_covco` value from 0.30 to 0.75 and updated its comment, 889136d made comment-only typo fixes in `ffcb`, `cdn`, and `eros_spl`, and f52e9d8 added `use utils` and changed the phosphorus normalization from `exp` to `exp_w`.

- df07e3f introduced the subroutine and its default assignments for basin parameters plus the derived uptake and output-lag values.
- 3bb22ed changed the fallback value for `bsn_prm%rsd_covco` from 0.30 to 0.75 and revised the comment to describe the C-factor equation.
- f52e9d8 added the `utils` dependency and replaced `exp(-bsn_prm%p_updis)` with `exp_w(-bsn_prm%p_updis)` for underflow-safe phosphorus normalization.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'basin_prm_default' has no extracted documentation comment.
