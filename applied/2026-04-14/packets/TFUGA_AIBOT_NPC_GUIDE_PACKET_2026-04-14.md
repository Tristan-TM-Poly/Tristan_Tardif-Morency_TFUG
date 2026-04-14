# TFUGA_AIBOT_NPC_GUIDE_PACKET — Applied Snapshot (2026-04-14)

## Purpose
Define the first bounded packet family for AI-BOT NPC guides inside TFUGA educational and exploratory game layers.

## NPC roles
- concept guide
- system guide
- experiment guide
- review guide
- collaboration guide

## Required packet members
- HumanPacket: what the NPC helps the player understand
- MachinePacket: npc_id, role, state, linked artifact families
- AIPacket: suggestion logic and adaptive hinting scope
- ReviewPacket: what the NPC may not unlock without gate approval
- PropagationPacket: where the player is routed next

## Law
An AI-BOT NPC guide is valid only if it increases bounded understanding and progression while staying coupled to packets, scores, and review constraints.
