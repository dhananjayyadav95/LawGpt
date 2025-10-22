# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added - 2024-01-XX
- **Query History Feature**: ChatGPT-style history management
  - In-memory storage on backend (stores last 50 queries per session)
  - localStorage backup on frontend (persists across page refreshes)
  - History survives page refreshes but clears on browser data clear
  - Ready for future database integration with user authentication
- Both text queries and research queries now appear in history
- Automatic history loading on app start

### Changed - 2024-01-XX
- Rolled back to commit 80ea714 (Enhanced Legal Response System)
- Disabled image upload feature (Photo tab)
- Disabled document upload feature (Document tab)
- Simplified UI to focus on core features: Query and Research tabs only

### Removed
- Streaming implementation and prompt optimization changes
- Image analysis functionality (temporarily disabled)
- Document upload functionality (temporarily disabled)

## Previous Versions

### Enhanced Legal Response System
- Implemented comprehensive legal response with action-first structure
- Added immediate actions, step-by-step solutions
- Included required documents and official forms
- Added similar case studies and warnings
- Success probability indicators
