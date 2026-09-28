# Jotter Architecture Overview

Jotter follows a clean, layered architecture to maintain clear boundaries between the user interface, business logic, and infrastructure details. 

## Dependency Flow

Dependencies must flow strictly inward:

```
CLI / Presentation (Typer, Rich)
       ↓
  Application (NoteService)
       ↓
    Domain (Note, Exceptions, Repository Protocol)
       ↑
 Infrastructure (SQLiteNoteRepository, SQLite Connection)
```

## Layers

### Domain
The `domain` layer holds the core entities (e.g. `Note`), domain-specific exceptions, and interface definitions (Protocols). It has absolutely no knowledge of how notes are stored, nor how they are rendered in the terminal.

### Application
The `application` layer coordinates the use-cases of Jotter. `NoteService` validates inputs, generates timestamps, and orchestrates calls to the repository. It bridges the gap between raw HTTP/CLI commands and domain entities.

### Infrastructure
The `infrastructure` layer manages operating-system and persistence concerns. 
- `database/`: Manages SQLite connections, PRAGMAs, schemas, and migrations via `user_version`.
- `repositories/`: Implements the `NoteRepository` protocol using raw SQLite queries.

### Presentation & CLI
- `presentation/`: Extracts formatting logic. JSON output and Rich table rendering live here, so the CLI commands remain thin.
- `cli/`: Uses Typer to parse arguments, setup dependency injection via `AppContext`, and route execution to services.

### Configuration
Centralizes path resolution using `platformdirs` and environment variables.

## Testing Strategy
- **Integration**: Tests database interactions directly using real temporary SQLite instances.
- **CLI**: Tests command execution, exit codes, and standard output rendering using Typer's `CliRunner`.
