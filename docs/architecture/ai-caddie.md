# AI Caddie Design

The AI caddie is one of Mercury's core features.

It should help during a round by recommending a club, target, and risk level for the current situation.

## Decision Boundary

Mercury informs decisions. Mercury does not make decisions.

The user remains the final authority.

## Inputs

The AI caddie should eventually understand:

- Player profile from `docs/golf-domain/player-profile.md`
- Current GPS position
- Current hole
- Distance to front, middle, and back green
- Pin position
- Hazards
- Wind
- Elevation
- Lie
- Stance
- Temperature
- Equipment setup
- Ball
- Club carry distances
- Club total distances
- Miss tendencies by club
- Confidence by club
- Player swing profile
- Recent round trends
- Score situation

## Outputs

The AI caddie should return:

- Recommended club
- Recommended target
- Risk level (should this be taken out? i think the user should be able to understand risk level themself? I just wonder if seeing risk level "high" would deter me from the shot always or avoid entirely any "high".)
- Short explanation
- Safer alternative when useful
- Aggressive alternative when useful

## Interface Pattern

During a round, the AI caddie should open from the hole map screen as a dialogue box or popover.

It should not force the user away from the current hole context.

The caddie popup should be fast, readable, and easy to dismiss.

## Example

Situation:

- 143 yards
- Front pin
- Water short
- 8 mph headwind
- Normal fairway lie

Recommendation:

- Smooth 9 iron
- Target center green
- Risk level: medium-low

Reason:

- Water short makes the front pin costly.
- Center green keeps a normal miss in play.
- The recommendation values expected score over attacking the pin.

## Early Recommendation Engine

The first version does not need advanced machine learning.

It can combine:

- Player-entered carry distances
- Known miss patterns
- Confidence ratings
- Basic wind adjustment
- Hazard awareness
- Conservative target rules

## Future Recommendation Engine

Later versions can use:

- Historical shot outcomes
- Strokes gained analysis
- Equipment comparisons
- Course-specific history
- Lie-specific tendencies
- R-generated analytics
- Model-based probability estimates

## Key Design Rule

The AI caddie should explain why it recommends something.

The explanation is part of the product, not an extra feature.

### Implementation mechanism (not yet decided until now)

Rather than hand-coding these as rigid if/then rules, the plan is a
direct LLM API call (e.g. Claude): assemble the inputs above into a
structured prompt, let the model reason through them in plain language.
This naturally supports the "explain why" requirement above, degrades
gracefully with sparse player data (a rules engine would need explicit
handling for every missing field; an LLM can reason around gaps), and
keeps the tone collaborative rather than a rigid lookup table.

MCP is not needed for this. MCP is for open-ended tool selection when
you don't know in advance what a model will need to look up. Here, the
inputs are fixed and known ahead of time -- our own backend gathers
them via normal queries and hands them to the model in one call. MCP
would add protocol complexity with no benefit at this stage. Revisit
only if the caddie becomes genuinely conversational (the golfer asks
follow-ups, the model decides what else to check).