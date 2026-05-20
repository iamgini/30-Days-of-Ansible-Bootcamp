# CLAUDE.md

This file provides guidance to Claude Code when working with this Ansible learning repository.

## Repository Overview

**30 Days of Ansible Bootcamp** is a comprehensive, community-focused educational project designed to teach Ansible from fundamentals to advanced concepts through a structured 30-day curriculum. This repository serves as the code companion to a YouTube video series and blog content.

**Project Purpose**: Enable learners to progress from zero Ansible knowledge to production-ready automation skills through hands-on examples, progressive lessons, and real-world use cases.

**Audience**: Beginners to intermediate DevOps engineers, system administrators, and automation enthusiasts learning Ansible.

**Format**: Multi-modal learning experience:
- **Video lessons**: YouTube playlist (techbeatly channel)
- **Written documentation**: README files with detailed explanations
- **Hands-on code**: Working playbooks, configurations, and examples
- **Practice exercises**: Real-world use cases

## Repository Structure

### Daily Lesson Organization (Day-01 through Day-30)

The repository contains 30 progressive lessons, each in its own directory:

```
Day-XX-Topic-Name/
├── README.md           # Lesson content, explanations, concepts
├── site.yaml          # Main example playbook (if applicable)
├── ansible.cfg        # Local Ansible configuration
├── inventory          # Sample inventory file
└── [additional files] # Supporting files (vars, templates, etc.)
```

**Learning Progression**:
- **Days 1-6**: Environment setup, installation, lab configuration
- **Days 7-10**: Fundamentals (inventory, ad-hoc commands, playbooks, privilege management)
- **Days 11-21**: Core concepts (modules, variables, facts, magic variables, vault/secrets)
- **Days 22-27**: Advanced control (loops, conditionals, handlers, failures, blocks, Jinja2)
- **Days 28-30**: Advanced topics (roles, parallelism, host patterns)

### Use Case Directories

Practical, real-world scenarios demonstrating specific Ansible applications:

- `Use-Case-Ansible-Variables/` - Variable management patterns
- `Use-Case-Calling-Role-with-Variable/` - Role parameterization
- `Use-Case-Collect-Host-Info/` - Fact gathering and reporting
- `Use-Case-Modify-JSON-YAML/` - Data manipulation
- `Use-Case-Vault-Advanced/` - Advanced secrets management with vault

Use cases include complete working examples with:
- Full playbook implementations
- Configuration files
- Sample data/variables
- vault-related scripts (for vault use cases)

### Work-in-Progress Content

`z_In_Prog/` - Contains draft lessons and experimental content:
- Lessons 7-12 (alternate numbering/organization)
- Content being developed or revised
- May not align with current day numbering

**Important**: This directory contains work that may be incomplete or superseded by content in the main Day-XX directories.

## Working with This Repository

### Running Examples

Each day's directory is **self-contained** with its own configuration:

```bash
# Navigate to specific day
cd Day-XX-Topic-Name/

# Run the example playbook
ansible-playbook site.yaml

# Or with explicit config
ansible-playbook -i inventory site.yaml
```

**Common Configuration Pattern**:
Most `ansible.cfg` files use:
```ini
[defaults]
inventory = ./inventory
remote_user = devops
host_key_checking = False
```

### Typical Inventory Format

Examples use simple INI-style inventories with test nodes:
```ini
node1.techbeatly.com
node2.techbeatly.com

[webservers]
node1.techbeatly.com

[databases]
node2.techbeatly.com
```

**Note**: These are example hostnames. Learners adapt these to their lab environment (VirtualBox/Vagrant VMs, cloud instances, etc.).

### Lab Environment Expectations

The curriculum assumes learners have set up a practice environment:
- **Control node**: Where Ansible is installed
- **Managed nodes**: 1-3 test systems (typically Linux)
- **Common setups**: VirtualBox + Vagrant (covered in Days 2-4), cloud VMs, containers

Most examples target:
- RHEL/CentOS-based systems (uses `yum` module)
- SSH-accessible nodes
- User `devops` with sudo privileges

## Content Development Guidelines

### When Adding or Modifying Lessons

**Maintain Progressive Learning**:
- Each day should build on previous concepts
- Avoid introducing advanced topics before prerequisites are covered
- Reference previous days when using earlier concepts

**Consistency Standards**:
1. **README Structure**: Start with YouTube video link, explain concept, show examples, provide full working code
2. **Playbook Style**:
   - Use descriptive task names
   - Include comments for complex logic
   - Follow YAML best practices (proper indentation, no tabs)
   - Start with `---`, ending `...` is optional
3. **File Naming**: Use `site.yaml` for main playbook, descriptive names for specialized playbooks
4. **Variables**: Use clear, descriptive variable names; document in README

**Code Quality for Teaching**:
- **Clarity over cleverness**: Choose readable code over concise-but-obscure patterns
- **Comment non-obvious behavior**: Explain *why*, not *what*
- **Show progression**: When showing multiple approaches, start simple then add complexity
- **Error handling**: In advanced lessons, demonstrate proper error handling; in basic lessons, keep it simple

### YouTube Video Integration

Each lesson references the associated video:
```markdown
[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)
```

**When updating lessons**:
- Ensure code matches what's shown in videos
- If code evolves beyond video, note the difference in README
- Keep video links current and functional

### Testing Changes

Before committing updates:
1. **Syntax check**: `ansible-playbook --syntax-check site.yaml`
2. **Dry run**: `ansible-playbook --check site.yaml` (if safe)
3. **Full test**: Run against test environment when possible
4. **README accuracy**: Verify README instructions match actual code
5. **Cross-lesson impact**: Check if changes affect later lessons that build on this content

### Common Patterns in This Repository

**Variable Examples**:
- Inline variables in playbook
- External var files (`vars.yaml`, `vars.yml`)
- Host vars and group vars (Day 14)
- Arrays/lists (Day 15)
- Registered variables (Day 16)
- Facts and magic variables (Days 17-19)

**Security/Vault Examples**:
- Encrypted files (`secret-data.yaml`, `secret-vars.yaml`, `user-passwd.yaml`)
- Vault password files
- Vault scripts (`vault.py`, `vault-pass-client.py`)

**Ansible.cfg Variations**:
- Basic configuration (most days)
- Roles path configuration (Day 28)
- Custom settings for specific lessons

## Repository Maintenance

### File Organization Rules

- **One concept per day**: Don't mix multiple major concepts in a single day
- **Self-contained examples**: Each day should run independently
- **No cross-day dependencies**: Avoid requiring files from other day directories
- **Shared resources**: If multiple days need the same file, duplicate it (keeps lessons independent)

### Avoiding Duplication Issues

While lessons are self-contained, ensure:
- Updated best practices propagate to all relevant days
- Security fixes apply across all examples
- Deprecated module usage is updated globally

### Version Considerations

**Ansible Version**: Examples should work with modern Ansible (2.9+), ideally Ansible Core 2.12+
**Module Evolution**: 
- Use FQCN (Fully Qualified Collection Names) when appropriate: `ansible.builtin.yum`
- Note when examples use older module syntax for compatibility
- Update deprecated modules across all days when identified

**Python Dependencies**: Some use cases may require:
- `jmespath` (for JSON queries)
- `PyYAML` (for YAML manipulation)
- `ansible-vault` (for vault operations)

## Educational Philosophy

This repository follows these teaching principles:

1. **Progressive Disclosure**: Introduce complexity gradually; don't overwhelm beginners
2. **Working Examples**: Every code snippet should be runnable, not pseudocode
3. **Real-World Relevance**: Use cases reflect actual automation scenarios
4. **Multiple Learning Styles**: Video + text + hands-on code
5. **Community-Focused**: Accessible to self-learners, free and open

## External Resources

- **YouTube Channel**: techbeatly
- **Video Playlist**: [Ansible Full Course](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)
- **License**: See LICENSE file (MIT License assumed based on GitHub best practices)

## Quick Reference: Topic Index

**Setup & Basics (Days 1-10)**:
- Day 1: Introduction to Ansible
- Days 2-6: Lab setup (VirtualBox, Vagrant, Installation)
- Day 7: Inventory management
- Day 8: Ad-hoc commands
- Day 9: Playbooks fundamentals
- Day 10: Remote user and privilege management

**Variables & Data (Days 11-19)**:
- Day 11: Finding modules
- Day 12: Managing variables
- Day 13: Extra variables
- Day 14: Host and group variables
- Day 15: Variable arrays
- Day 16: Registered variables
- Day 17: Ansible facts
- Day 18: Custom facts
- Day 19: Magic variables

**Security (Days 20-21)**:
- Day 20: Ansible vault basics
- Day 21: Using secrets in playbooks

**Control Structures (Days 22-27)**:
- Day 22: Task control and loops
- Day 23: Conditional execution
- Day 24: Handlers
- Day 25: Task failure handling
- Day 26: Blocks
- Day 27: Jinja2 templating

**Advanced Topics (Days 28-30)**:
- Day 28: Roles
- Day 29: Parallelism
- Day 30: Host patterns

## Working with Claude Code

**When asked to help with lessons**:
- Maintain the educational tone and progressive learning approach
- Ensure code is beginner-friendly and well-commented
- Test examples when possible before suggesting changes
- Consider impact on learners following the video series
- Keep examples realistic but simple enough for learning

**When creating new content**:
- Follow the established day structure
- Create self-contained, runnable examples
- Write README with clear explanations
- Link to relevant earlier days for prerequisites
- Consider where it fits in the 30-day progression

**When debugging examples**:
- Remember the target audience is learning Ansible
- Explain fixes in educational terms
- Update README if the fix changes the learning point
- Check if similar issues exist in other days
