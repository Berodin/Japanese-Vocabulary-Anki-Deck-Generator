import genanki
import csv
import os
from merge_data import merge_data
from anki_model import get_model

def create_deck(lc):
    merged_file = merge_data(lc)
    if not merged_file:
        print(f"Skip deck creation: No merged file found for '{lc}'.")
        return 

    model_id = 1607392319
    model = get_model(model_id, lc)

    deck = genanki.Deck(model_id, f'Japanese Vocab Deck ({lc})')
    package = genanki.Package(deck)

    # Add data
    with open(merged_file, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Reading Card
            reading_fields = [
                row['expression'],              # Expression
                row['meaning'],                 # Meaning
                row['reading'],                 # Reading
                row['sentence'],                # Sentence
                row['sentence_kana'],           # SentenceKana
                row.get('sentence_translation', ''),  # SentenceTranslation (optional)
                f'[sound:{row["sentence_audio"]}]' if row['sentence_audio'] else '',  # SentenceAudio (optional)
                f'[sound:{row["expression_audio"]}]' if row['expression_audio'] else '',  # ExpressionAudio
                row["image_uri"] if row["image_uri"] else ''  # ImageURI (optional)
            ]
            reading_note = genanki.Note(
                model=model,
                fields=reading_fields
            )
            deck.add_note(reading_note)

            # Listening Card (only if ExpressionAudio is provided)
            if row["expression_audio"]:
                listening_fields = [
                    row['expression'],              # Expression
                    row['meaning'],                 # Meaning
                    row['reading'],                 # Reading
                    row['sentence'],                # Sentence
                    row['sentence_kana'],           # SentenceKana
                    row.get('sentence_translation', ''),  # SentenceTranslation (optional)
                    f'[sound:{row["sentence_audio"]}]' if row['sentence_audio'] else '',  # SentenceAudio (optional)
                    f'[sound:{row["expression_audio"]}]',  # ExpressionAudio
                    row["image_uri"] if row["image_uri"] else ''  # ImageURI (optional)
                ]
                listening_note = genanki.Note(
                    model=model,
                    fields=listening_fields
                )
                deck.add_note(listening_note)

            # Add media files
            if row["sentence_audio"]:
                sentence_audio_path = f"data/audio/{row['sentence_audio']}"
                if os.path.exists(sentence_audio_path):
                    package.media_files.append(sentence_audio_path)
                else:
                    print(f"Warning: Audio file not found: {sentence_audio_path}")

            if row["expression_audio"]:
                expression_audio_path = f"data/audio/{row['expression_audio']}"
                if os.path.exists(expression_audio_path):
                    package.media_files.append(expression_audio_path)
                else:
                    print(f"Warning: Audio file not found: {expression_audio_path}")

            if row["image_uri"]:
                image_path = f"data/images/{row['image_uri']}"
                if os.path.exists(image_path):
                    package.media_files.append(image_path)
                else:
                    print(f"Warning: Image file not found: {image_path}")

    # Save deck
    os.makedirs("output", exist_ok=True)
    output_file = f'output/japanese_vocab_{lc}.apkg'
    package.write_to_file(output_file)
    print(f"Deck created: {output_file}")

if __name__ == "__main__":
    create_deck("de")
