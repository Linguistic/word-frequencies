proto_out := "./proto"

@start +args:
  poetry run python -m word_counter.main {{args}}

@cheat lang:
  poetry run python -m word_counter.cheat {{lang}}

proto:
  protoc -I {{proto_out}} --python_out={{proto_out}} --pyi_out={{proto_out}} ./proto/frequency.proto