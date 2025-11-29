from fastapi import APIRouter, Header, HTTPException
from app.services.huggingface_service import query
from app.schemas.TextRequest import TextRequest
from app.auth.token_auth import verify_token 


router = APIRouter(prefix="/traduction", tags=["traduction du texte"])


@router.post("/traduire/fr-en")
async def traduire_fr_vers_en(data: TextRequest, token: str = Header(...)):
    """
    Traduit un texte du français vers l'anglais.
    Nécessite un token JWT valide dans le header 'token'.
    """
    try:
        # Vérification du token JWT
        verify_token(token)
        
        # Traduction FR → EN
        result = query(data.text,"Helsinki-NLP/opus-mt-fr-en")
        
        return {
            "success": True,
            "direction": "fr-en",
            "original_text": data.text,
            "translated_text": result
        }
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur lors de la traduction FR→EN: {str(e)}"
        )


@router.post("/traduire/en-fr")
async def traduire_en_vers_fr(data: TextRequest, token: str = Header(...)):
    """
    Traduit un texte de l'anglais vers le français.
    Nécessite un token JWT valide dans le header 'token'.
    """
    try:
        # Vérification du token JWT
        verify_token(token)
        
        # Traduction EN → FR
        result = query(data.text,"Helsinki-NLP/opus-mt-en-fr")
        
        return {
            "success": True,
            "direction": "en-fr",
            "original_text": data.text,
            "translated_text": result
        }
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur lors de la traduction EN->FR: {str(e)}"
        )