package kamilsedrowicz.example.spring;

import org.springframework.web.bind.annotation.*;

import java.util.HashMap;

@RestController
@RequestMapping(value = "/rest/ad")
class AdService {

    @RequestMapping(value = "/", method = RequestMethod.GET)
    public HashMap<Long, Ad> getAllAds() {
        return AdApplication.adsBoard;
    }

    @RequestMapping(value = "/add", method = RequestMethod.POST)
    public Ad addAd(@RequestParam(value = "title") String title
            , @RequestParam(value = "description", defaultValue = "no description") String description) {

        Ad ad = new Ad(title, description);
        AdApplication.adsBoard.put(ad.getId(), ad);
        return ad;
    }

    @RequestMapping(value = "/update", method = RequestMethod.PUT)
    public Ad updateAd(@RequestBody Ad ad) throws Exception {
        if (AdApplication.adsBoard.containsKey(ad.getId())) {
            AdApplication.adsBoard.put(ad.getId(), ad);
        } else {
            throw new Exception("Ad " + ad.getId() + " does not exists");
        }
        return ad;
    }

    @RequestMapping(value = "/delete/{id}", method = RequestMethod.DELETE)
    public Ad deleteAd(@PathVariable long id) throws Exception {

        Ad ad;
        if (AdApplication.adsBoard.containsKey(id)) {
            ad = AdApplication.adsBoard.get(id);
            AdApplication.adsBoard.remove(id);
        } else {
            throw new Exception("Ad " + id + " does not exists");
        }
        return ad;
    }

    @RequestMapping(value = "/{id}", method = RequestMethod.GET)
    public Ad getAd(@PathVariable long id) {
        return AdApplication.adsBoard.get(id);
    }
}